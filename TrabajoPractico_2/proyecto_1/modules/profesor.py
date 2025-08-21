from modules.persona import Persona

class Profesor(Persona): 
    '''Profesor modela un profesor que puede enseñar en los cursos de una facultad'''
    def __init__(self, nombre, edad): 
        '''lista de los cursos donde enseña.'''
        self.__cursos = [] 
        '''lista de los departamentos de los que forma parte.'''
        self.__departamentos = [] 
        super().__init__(nombre, edad)
        '''inicialmente un profesor no es director.'''
        self.__es_director = False
        '''si fuera director, este es el departamento del cual es director.'''
        self.__dptm_director = None 

    def set_cursos(self, p_curso): 
        ''' Vamos a cargar el vector de los cursos cuando la facultad crea el curso nuevo. '''
        self.__cursos.append(p_curso)
    
    def set_departamentos(self, departamento):
        '''Actualizamos la lista de departamentos de los que forma parte'''
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento) #También añade este departamento a la lista 
            #general de departamentos a los que pertenece el profesor, si no lo estaba ya.

    def set_es_director(self):
        '''Actualizar el valor booleano del profesor''' # indicando que este profesor ha sido nombrado director.
        self.__es_director = True

    def set_dptm_director(self, departamento):
        '''Actualizamos el valor del departamento del director'''
        self.__dptm_director = departamento
        self.__departamentos.append(self.__dptm_director)

    def get_es_director(self):
        '''Informamos si es director o no'''
        return self.__es_director

    def get_info(self):
        '''Se muestra la informacion del profesor, retorna un str con esa informacion'''
        cursos = [curso.get_nombre() for curso in self.__cursos]
        departamentos = [departamento.get_nombre_dpt() for departamento in self.__departamentos]

        return f"Nombre: {self._nombre}, Edad: {self._edad}, cursos: {', '.join(cursos)}, departamentos: {', '.join(departamentos)}, ¿Es director?: {self.__es_director}"


