from modules.profesor import Profesor
from modules.estudiante import Estudiante

class Curso:
    def __init__ (self, nombre_c, profesor:Profesor):   
        '''Curso representa un curso que forma parte de una facultad.
        - Cuando se crea un nuevo curso, debe tener un profesor que enseñe en él.
        - enseña en... representado por una lista de profesores que enseñan en ese curso.
        - asiste a... representado por una lista de estudiantes que asisten a ese curso'''
        self.__catedra = [profesor]  # lista de profesores
        self.__inscriptos = []       # lista de estudiantes
        self.__nombre = nombre_c
        self.__departamento = None

    def set_catedra(self, profesor:Profesor):
        '''Agregar profesor a la cátedra'''
        self.__catedra.append(profesor)
    
    def set_departamento(self, departamento):
        self.__departamento = departamento
    
    def get_nombre_dpt(self):
        '''Retorna el nombre del departamento asociado'''
        if self.__departamento is not None:
            return self.__departamento.get_nombre_dpt()
        else:
            return None 
   
    def set_inscriptos(self, estudiante:Estudiante):
        '''Inscribir un estudiante en el curso'''
        self.__inscriptos.append(estudiante)
        
    def set_nombre(self, nombre_c):
        '''Establecer el nombre del curso'''
        self.__nombre = nombre_c
    
    def get_nombre(self): 
        '''Retorna el nombre del curso'''
        return self.__nombre
    
    def get_profesor(self):
        '''Retorna el primer profesor de la cátedra'''
        if self.__catedra:
            return self.__catedra[0]
        
        return None

