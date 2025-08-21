from modules.persona import Persona 

class Estudiante(Persona):
    '''Estudiante modela un estudiante que puede asistir a los cursos de una facultad'''
    def __init__(self, nombre, edad): 
                '''Cursos_asistidos es una lista de objetos Curso'''
                self.__cursos_asistidos = [] 
                super().__init__(nombre, edad)


                
    def get_info(self):
                '''Mostramos la informacion del estudiante, retorna un str con esa informacion'''
                cursos = [curso.get_nombre() for curso in self.__cursos_asistidos]
                return f"Nombre: {self._nombre}, Edad: {self._edad}, cursos: {', '.join(cursos)}"


    def set_cursos_asistidos(self, p_curso): 
                #Permite a la Facultad registrar un curso al que el estudiante asiste.
                '''Es una lista donde se guardan los objetos Curso a los que el estudiante se inscribe.''' 
                self.__cursos_asistidos.append(p_curso)
              