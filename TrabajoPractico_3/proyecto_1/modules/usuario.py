import uuid
from abc import ABC

class Usuario(ABC):
    '''Clase Usuario, nos permite manejar todos los atributos y metodos correspondientes a un usuario'''
    def __init__(self,nombre:str,apellido:str,contrasenia,nombre_usuario:str, email:str):
        self._nombre = nombre 
        self._apellido = apellido
        self._nombre_usuario = nombre_usuario
        self._contrasenia = contrasenia
        self._email = email
        '''Generar un UUID único. entero. de 64 bits:'''
        self.__id = uuid.uuid4().int & (1<<63)-1  
        
     
    def get_nombre_usuario(self):
        return self._nombre_usuario
    
    def get_contrasenia(self):
        return self._contrasenia
    
    def get_email(self):
        return self._email
    
    def get_nombre(self):
        return self._nombre
    
    def get_apellido(self):
        return self._apellido
    
    def get_id(self):
        return self.__id
    
    def set_id(self, nuevo_id):
        self.__id = nuevo_id