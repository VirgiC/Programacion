import uuid
from datetime import datetime

class Reclamo:
    def __init__(self, contenido:str):
        '''Un reclamo por defecto, si pasa los controles y es creado, se setea en pendiente.'''
        self.__estado_actual = "pendiente"
        '''Generar un UUID único. entero. de 64 bits:'''
        self.__id = uuid.uuid4().int & (1<<63)-1  
        self.__contenido = contenido
        '''Inicialmente, no tiene un departamento en particular, pasa por un proceso de clasificacion'''
        self.__departamento = None
        ahora  = datetime.now()
        '''Fecha y hora en nuestro formato en el que se creo el reclamo'''
        self.__fecha_y_hora = str(ahora.strftime('%d/%m/%Y %H:%M:%S'))
        
    def set_departamento(self, nuevo_departamento):
        self.__departamento = nuevo_departamento

    def set_estado_actual(self,estado_id):
        self.__estado_actual = estado_id

    def set_id(self,id):
        self.__id = id
    
    def set_fecha_y_hora(self,fecha):
        self.__fecha_y_hora = fecha

    def get_estado_actual(self):
        estado = self.__estado_actual
        return estado
    
    def get_id(self):
        id = self.__id
        return id

    def get_fecha_y_hora(self):
        timestamp = self.__fecha_y_hora
        return timestamp
    
    def get_contenido(self):
        contenido = self.__contenido
        return contenido
    
    def get_nombre_departamento(self):
        nombre = self.__departamento 
        return nombre
    



 