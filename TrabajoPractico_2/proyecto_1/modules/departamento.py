from modules.profesor import Profesor

class Departamento: 
    def __init__(self, profesor:Profesor, nombre:str): #recibe una instancia de profesor como parametro
        '''Clase departamento representa un departamento que conforma a la facultad.
        profes es una lista de objetos Profesor que estan asignados a ese departamento.
        cursos es una lista de objetos Curso que estan asociados al departamento'''
        self.__profes = []
        self.__director = profesor #la almacena como un atributo 
        self.__nombre_dpt = nombre
        self.__cursos = []  
   
    def set_profes(self, profesor:Profesor):
        '''Cargar la lista de profesores del departamento'''
        self.__profes.append(profesor)

    def set_cursos(self, curso):
        '''Cargar la lista de cursos'''
        self.__cursos.append(curso)
    
    def get_profes(self):
        '''Retorna la lista con los nombres los profesores'''
        return self.__profes.get_nombre()
    
    def cant_cursos(self):
        '''Retorna la cantidad de cursos'''
        return len(self.__cursos)
    
    def get_director(self):
        '''Retorna el nombre del director'''
        return self.__director.get_nombre()

    
    def get_nombre_dpt(self):
        '''Retorna el nombre del departamento'''
        return self.__nombre_dpt
    
    def get_nombre_cursos(self):
        '''Retorna un str con los cursos asociados a ese departamento, indexados'''
        info_cursos = ""
        i = 1
        for curso in self.__cursos:
            info_cursos += f"{i} - {curso.get_nombre()}\n"
            i += 1
        return info_cursos
        
    
    