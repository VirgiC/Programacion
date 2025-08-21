from sqlalchemy import func
from werkzeug.security import generate_password_hash
import os
from modules.models import TablaReclamos, TablaUsuario, asociacion_usuarios_reclamos
from modules.reclamo import Reclamo
from modules.cliente import Cliente
from modules.jefe_departamento import JefeDeDepartamento
from modules.secretario_tecnico import SecretarioTecnico
from modules.usuario import Usuario
from flask_sqlalchemy import SQLAlchemy


class GestorDB: 
    def __init__(self,db: SQLAlchemy): 
        '''GestorDB es una clase que posee todas las funcionalidades necesarias para trabajar con nuestra Base de Datos'''
        self.__db = db
        self.__db.create_all()
    
    def cant_reclamos_totales(self):
        '''Contamos la cantidad de reclamos que hay en la tabla con query.count'''
        return(TablaReclamos.query.count())
    
    def cargar_administradores_desde_archivo(self, archivo_txt):
        '''Esta funcion permite crear los administradores a partir de un .txt, para no tener que estar creandolos nosotros 
        a partir del registro'''
        ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'data', archivo_txt)
        administradores = []

        with open(ruta_archivo, 'r',encoding='utf-8') as file:
            lineas = file.readlines()
            for linea in lineas:
                nombre, apellido, email, contrasenia, username, id_administrador, departamento = linea.strip().split(',')
                '''Creamos el usuario administrador'''
                encripted_pass = generate_password_hash(password= contrasenia,method= 'pbkdf2:sha256',salt_length=8 )
                if departamento == "secretaría técnica":
                    nuevo_admin = SecretarioTecnico(nombre, apellido, encripted_pass, username, email)
                else:
                    nuevo_admin = JefeDeDepartamento(nombre, apellido, encripted_pass, username, email)
                
                '''Seteamos el id'''
                nuevo_admin.set_id(id_administrador)
                '''Guardamos en la base de datos'''
                self.cargar_usuario(nuevo_admin)
                '''Agregamos el administrador y su departamento a la lista'''
                administradores.append((id_administrador, departamento))
    
        return administradores

    def todos_los_reclamos(self, departamento=None):
        '''reclamos_filas es una lista de objetos que cada elemento de la lista es una fila de TablaReclamos, 
        esa fila es un objeto del tipo TablaReclamos, podemos pensarlo una subtabla'''
        if departamento == None:
            reclamos_filas= self.__db.session.query(TablaReclamos).all()
        else:
            reclamos_filas = self.__db.session.query(TablaReclamos).filter_by(departamento=departamento).all()
        reclamos_objetos = []
        '''recorremos todos los elementos de reclamos_filas, fila=reclamos_filas[0]'''
        for fila in reclamos_filas:
            reclamo = Reclamo(fila.contenido)
            reclamo.set_estado_actual(fila.estado)
            reclamo.set_id(fila.id)
            reclamo.set_departamento(fila.departamento)
            reclamo.set_fecha_y_hora(fila.fecha)

            ''' ID del usuario que creó el reclamo '''
            id_usuario_creador = fila.id_usuario

            ''' Obtener los IDs de los adherentes (seguidores) del reclamo '''
            adherentes = [usuario.id for usuario in fila.usuarios_seguidores]
            dias = fila.dias

            ''' Añadir una tupla con el objeto Reclamo, el ID del usuario creador y los IDs de los adherentes ''' 
            reclamos_objetos.append((reclamo, id_usuario_creador, adherentes, dias))

        return reclamos_objetos

    def actualizar_campos(self, id_fila, campos_actualizar):
        ''' Obtener la fila que se desea actualizar, filtramos por ese id de la fila y con first() encontramos la primera
        coincidencia'''
        fila = self.__db.session.query(TablaReclamos).filter_by(id=id_fila).first()
        ''' Actualizar los valores de las columnas en la fila específica'''
        if fila:
            '''campos_actualizar es un diccionario que contiene pares clave-valor donde la clave es el nombre 
            del campo que se desea actualizar en la fila (for campo) y el valor es el nuevo valor que se desea asignar (,valor).'''
            for campo, valor in campos_actualizar.items():
                '''setattr es una funcion permite establecer dinamicamente los atributos de un objeto, para el objeto fila, actualiza
                el campo y el valor'''
                setattr(fila, campo, valor)
            
            ''' Guardar los cambios en la base de datos '''
            self.__db.session.commit()

    def cargar_reclamo(self,reclamo:Reclamo,  cliente_id: int): 
        '''Carga el reclamo que recibe como parametro en la base de datos si es que no existe ya en esta'''
        ''' Verificar si el reclamo ya existe en la base de datos '''
        reclamo_existente = self.__db.session.query(TablaReclamos).filter_by(contenido=reclamo.get_contenido()).first()
        if reclamo_existente:
            '''El reclamo ya existe en la base de datos.'''
            return
        
        '''Creamos el nuevo_reclamo, lo cargamos en la DB y hacemos un commit de los cambios'''
        nuevo_reclamo = TablaReclamos(
        contenido = reclamo.get_contenido(),
        departamento = reclamo.get_nombre_departamento(),
        id = reclamo.get_id(),
        estado = reclamo.get_estado_actual(),
        id_usuario = cliente_id,
        fecha = reclamo.get_fecha_y_hora() )
        
        self.__db.session.add(nuevo_reclamo)
        self.__db.session.commit()
        usuario = self.consultar_usuario('id',cliente_id)
        usuario.reclamos_seguidos.append(nuevo_reclamo)
        self.__db.session.commit()

    def cargar_usuario(self, usuario: Usuario):
        
            ''' Verificar si el usuario ya existe en la base de datos '''
            usuario_existente = self.__db.session.query(TablaUsuario).filter_by(username=usuario.get_nombre_usuario()).first()
            if usuario_existente:
                '''El usuario ya existe en la base de datos'''
                return
            
            '''Creamos el usuario, lo agregamos y actualizamos la base de datos'''
            nuevo_usuario = TablaUsuario(
                nombre = usuario.get_nombre(),
                apellido = usuario.get_apellido(),
                email = usuario.get_email(),
                contrasenia = usuario.get_contrasenia(),
                username = usuario.get_nombre_usuario(),
                id = usuario.get_id(),
                claustro = '')

            ''' Verificar si el usuario es una instancia de Cliente '''
            if isinstance(usuario, Cliente):
                nuevo_usuario.claustro = usuario.get_claustro()

            self.__db.session.add(nuevo_usuario)
            self.__db.session.commit()
 
    def adherir_usuario_a_reclamo(self, id_usuario, id_reclamo):
        '''Actualizamos la base de datos con la asociacion de el usuario que se adhiere a un reclamo'''
        '''Filtramos por ID usuario y ID reclamo'''
        usuario = TablaUsuario.query.filter_by(id=id_usuario).first()
        reclamo = TablaReclamos.query.filter_by(id=id_reclamo).first()
        if usuario and reclamo:
            ''' Verificar que el usuario no esté ya en la lista de adheridos '''
            if usuario not in reclamo.usuarios_seguidores:
                '''Si no esta, añadimos el reclamos a los reclamos del usuario'''   
                usuario.reclamos_seguidos.append(reclamo)
                '''Actualizamos la DB'''
                self.__db.session.commit()

    def obtener_reclamos_por_usuario(self, user_id):
        '''Recibe el id del usuario como parametro y retorna una lista de objetos Reclamo que fueron creados
        por el mismo y los adheridos'''
        lista_tabla = []

        reclamos_filas = self.__db.session.query(asociacion_usuarios_reclamos).filter_by(user_id=user_id).all()
        #obtenemos los id de los reclamos
        reclamo_ids = [fila.reclamo_id for fila in reclamos_filas]

        for id in reclamo_ids:
            tabla_reclamo = self.__db.session.query(TablaReclamos).filter_by(id = id).first()
            lista_tabla.append(tabla_reclamo)

        reclamos_objetos = []
        
        for tabla_reclamo in lista_tabla:
            reclamo = Reclamo(tabla_reclamo.contenido)
            reclamo.set_estado_actual(tabla_reclamo.estado)
            reclamo.set_id(tabla_reclamo.id)
            reclamo.set_departamento(tabla_reclamo.departamento)
            reclamo.set_fecha_y_hora(tabla_reclamo.fecha)
            reclamos_objetos.append(reclamo)  
        return reclamos_objetos
    
    def obtener_dias_segun_estado(self, estado):
        '''Recibe el estado de los reclamos y retorna la lista con la cantidad de dias de resolucion para los reclamos en un estado en particular'''
        reclamos_filas = (self.__db.session.query(TablaReclamos).filter_by(estado=estado)).all()
        dias_list = []

        for fila in reclamos_filas:
            if hasattr(fila, 'dias') and fila.dias is not None: 
                ''' Verificar si la fila tiene el atributo 'dias' y que no sea None '''
                dias_list.append(fila.dias)

        return dias_list
    
    def obtener_reclamos_pendientes(self, departamento=None):
        ''' Recibe como parametro opcional el departamento por el cual se quiere filtrar los reclamos y retorna una lista de tuplas
        El primero elemento de cada tupla es un objeto Reclamo (que corresponde a ese departamento), y el
        segundo elemento de la tupla es la cantidad de adheridos '''
        reclamos_query = self.__db.session.query(TablaReclamos).filter_by(estado='pendiente')
        
        if departamento and departamento != 'todos':
            reclamos_query = reclamos_query.filter_by(departamento=departamento)
            
        reclamos_filas = reclamos_query.all()
        reclamos_objetos = []

        for fila in reclamos_filas:
            reclamo = Reclamo(fila.contenido)
            reclamo.set_estado_actual(fila.estado)
            reclamo.set_id(fila.id)
            reclamo.set_departamento(fila.departamento)
            reclamo.set_fecha_y_hora(fila.fecha)

            ''' Obtener el número de adherentes para el reclamo actual '''
            num_adherentes = self.__db.session.query(func.count(asociacion_usuarios_reclamos.c.user_id)).filter_by(reclamo_id=fila.id).scalar()

            reclamos_objetos.append((reclamo, num_adherentes))

        return reclamos_objetos
    
    def todos_los_estados(self):
        '''Retorna una lista con los estados de todos los reclamos de la base de datos'''
        estados = self.__db.session.query(TablaReclamos.estado).all()
        return estados
    
    def todos_los_contenidos(self):
        ''' Retorna un string con el contenido de todos los reclamos'''
        resultado = ""
        contenidos = self.__db.session.query(TablaReclamos.contenido).all()
        for contenido in contenidos:
            resultado += " " + contenido[0] 
        return resultado
 
    def consultar_usuario(self, filtro, valor_filtro):
        if filtro == 'email':
            return TablaUsuario.query.filter_by(email=valor_filtro).first()
        elif filtro == 'id':
            return TablaUsuario.query.filter_by(id=valor_filtro).first()
        else:
            return None  

    