import os
import matplotlib
matplotlib.use('Agg') # <--- Añade esta línea para usar un backend no interactivo
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from modules.gestor_db import GestorDB
from modules.reclamo import Reclamo
from modules.clasificador import Clasificador
from modules.monticulo_mediana import MonticuloMediana
from modules.config import app # <--- ¡Importa 'app' aquí para usar app.root_path!

class GestorReclamo:
    # Principal interfaz para todas las operaciones relacionadas con los reclamos
    def __init__(self, gestor_db: GestorDB):
        '''GestorReclamo es una clase que posee todas las funcionalidades necesarias para trabajar 
        con nuestros reclamos.'''
        self.gestor_db = gestor_db

    def crear_reclamo(self, contenido):
        '''Recibe el contenido de un reclamo, lo clasifica y retorna un objeto Reclamo'''
        reclamo = Reclamo(contenido)
        clasificador = Clasificador()
        '''Obtener el primer elemento de la lista'''
        departamento = clasificador.clasificar_reclamo(contenido)[0]  # obtener el departamento de un nuevo reclamo
        reclamo.set_departamento(departamento)
        return reclamo

    def guardar_reclamo(self, reclamo, id_usuario):
        self.gestor_db.cargar_reclamo(reclamo, id_usuario)

    def reclamos_pendientes(self, departamento=None):
        ''' Recibe como parametro opcional el departamento por el cual se quiere filtrar los reclamos,
        Desglosa la informacion de cada reclamo dada por la instancia de GestorDB y retorna una lista de tuplas
        (id, estado actual, fecha y hora, contenido, nombre del departamento al que pertenece, y el numero de adherentes)'''
        informacion = self.gestor_db.obtener_reclamos_pendientes(departamento)

        resultado = []
        for reclamo, num_adherentes in informacion:
            # Desglosamos la informacion del reclamo
            id = reclamo.get_id()
            estado_actual = reclamo.get_estado_actual()
            fecha_y_hora = reclamo.get_fecha_y_hora()
            contenido = reclamo.get_contenido()
            nombre_departamento = reclamo.get_nombre_departamento()

            resultado.append((id, estado_actual, fecha_y_hora, contenido, nombre_departamento, num_adherentes))
            # Agregamos la tupla al resultado
        return resultado

    def actualizar_campos(self, reclamo_id, campos):
        '''Actualiza la base de datos segun corresponda, recibiendo el id del reclamo y el campo 
        a actualizarse'''
        self.gestor_db.actualizar_campos(reclamo_id, campos)

    def mis_reclamos(self, id_usuario):
        '''Recibe el id del usuario y retorna una lista de tuplas con la informacion de cada reclamo 
        que quiero mostrar: (id, estado actual y contenido) Estos reclamos son los creados por el usuario
        y a los que se adhirio'''
        reclamos = self.gestor_db.obtener_reclamos_por_usuario(id_usuario)
        resultado = []
        for reclamo in reclamos:
            id = reclamo.get_id()
            estado_actual = reclamo.get_estado_actual()
            contenido = reclamo.get_contenido()

            resultado.append((id, estado_actual, contenido))
        return resultado

    def cant_reclamos_tot(self):
        return self.gestor_db.cant_reclamos_totales()

    def todos_los_reclamos(self, departamento=None):
        '''Retorna una lista de tuplas con la informacion de todos los reclamos, por cada reclamo:
        (id, nombre_departamento, contenido, estado_actual, fecha_y_hora, id_usuario_creador, adherentes y dias)'''
        informacion = self.gestor_db.todos_los_reclamos(departamento)
        resultado = []
        for reclamo, id_usuario_creador, adherentes, dias in informacion:
            id_reclamo = reclamo.get_id()
            nombre_departamento = reclamo.get_nombre_departamento()
            contenido = reclamo.get_contenido()
            estado_actual = reclamo.get_estado_actual()
            fecha_y_hora = reclamo.get_fecha_y_hora()

            resultado.append((id_reclamo, nombre_departamento, contenido, estado_actual, fecha_y_hora, id_usuario_creador, adherentes, dias))

        return resultado

    def dias_segun_estado(self, estado):
        return self.gestor_db.obtener_dias_segun_estado(estado)

    def adherir_usuario(self, id_usuario, id_reclamo):
        return self.gestor_db.adherir_usuario_a_reclamo(id_usuario, id_reclamo)

    def mostrar_mediana(self, monticulo_mediana: MonticuloMediana):
        return monticulo_mediana.get_mediana()

    def actualizar_mediana(self, monticulo_mediana: MonticuloMediana, elemento):
        monticulo_mediana.actualizar_mediana(elemento)

    def grafico_circular(self):
        # gráfico circular que muestra la proporción de reclamos en los diferentes
        # estados (pendiente, en proceso, resuelto)

        pendiente = 0
        proceso = 0
        resuelto = 0

        '''Consulta todos los estados de reclamos desde la base de datos, esto lo hace a traves de GestorDb'''
        todos_los_estados = self.gestor_db.todos_los_estados()

        for estado in todos_los_estados:
            if estado[0] == "pendiente":
                pendiente += 1
            elif estado[0] == "en proceso":
                proceso += 1
            elif estado[0] == "resuelto":
                resuelto += 1

        '''Crear el gráfico circular'''
        labels = ['Pendiente', 'En Proceso', 'Resuelto']
        sizes = [pendiente, proceso, resuelto]
        colors = ['lightblue', 'lightcoral', 'lightgreen']

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Proporción de reclamos')

        #  Ruta absoluta usando app.root_path
        ruta_guardado_circular = os.path.join(app.root_path, 'static', 'grafico_circular.png')
        plt.savefig(ruta_guardado_circular)
        plt.close() # Cierra la figura para liberar memoria

    def grafico_palabras(self):

        '''Genera un grafico de palabras mas repetidas en los reclamos'''
        string_concatenado = self.gestor_db.todos_los_contenidos()

        stop_words = stopwords.words("spanish")

        nube = WordCloud(stopwords=stop_words,
                         max_words=15,
                         width=1000,
                         height=200).generate(string_concatenado)
        # WordCloud= este método crea una nube de palabras a partir de los contenidos de todos los reclamos
        # la palabra (reclamo) mas frecuente, tendra un mayor tamaño


        # <--- Ruta absoluta usando app.root_path
        ruta_guardado = os.path.join(app.root_path, 'static', 'grafico_palabras.png')

        ''' Guarda la nube de palabras en el archivo especificado'''
        nube.to_file(ruta_guardado)

        plt.title('Nube de palabras')
        plt.imshow(nube, interpolation='bilinear')
        plt.axis("off")
        plt.close() # Cierra la figura para liberar memoria