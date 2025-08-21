from modules.gestor_db import GestorDB
from modules.cliente import Cliente

class GestorUsuario: 
    def __init__(self, gestor_db:GestorDB): 
        '''GestorUsuario es una clase que se encarga de todas las operaciones relacionadas
         a los usuarios que usan el sistema de reclamos, ya sean clientes o administradores'''
        self.gestor_db = gestor_db

    def crear_cliente(self, nombre, apellido, contrasenia, nombre_usuario, claustro, mail):
        cliente = Cliente(
            nombre = nombre,
            apellido = apellido,
            contrasenia = contrasenia,
            nombre_usuario = nombre_usuario,
            claustro = claustro,
            mail = mail
        )
        self.guardar_usuario(cliente)
    
    def consultar_usuario(self,filtro, valor_filtro):
        '''Consulta un usuario en la base de datos, el filtro puede ser id, nombre_usuario o mail'''
        user = self.gestor_db.consultar_usuario(filtro,valor_filtro)
        return user
    
    def cargar_administradores(self, archivo):
        '''Carga los administradores, cuya informacion se encuentra en el archivo, en la base de datos.
        Retorna una lista de tuplas(id_administrador, departamento)'''
        lista = self.gestor_db.cargar_administradores_desde_archivo(archivo)
        return lista
    
    def guardar_usuario(self, usuario):
        '''Guarda el usuario en la base de datos'''
        self.gestor_db.cargar_usuario(usuario)
     
    


