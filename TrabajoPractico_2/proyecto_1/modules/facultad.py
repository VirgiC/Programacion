from modules.estudiante import Estudiante
from modules.profesor import Profesor
from modules.departamento import Departamento
from modules.curso import Curso
from random import *

class Facultad: 
    def __init__(self, nombre_depto1:str, director:Profesor): 
        '''Facultad representa una institucion compuesta por departamentos y cursos.
        La facultad necesita para su creacion un departamento y a la vez, el departamento necesita un profesor.
        profes_facu: Lista de objetos Profesor, se cargan haciendo uso de contratar_profesor
        estudiantes_facu: Lista de objetos Estudiante, se cargan haciendo uso de inscribir_alumno
        departamentos: Lista de objetos Departamento, se cargan haciendo uso de crear_departamento
        cursos: Lista de objetos Curso, se cargan haciendo uso de crear_curso'''
        self.__profes_facu = [director] 
        self.__estudiantes_facu = [] 
        self.__departamentos = [] 
        self.__cursos = [] 
        # Ahora el constructor llama al nuevo crear_departamento
        self.crear_departamento(nombre_depto1, director) 

    def inscribir_alumno(self, alumno:Estudiante): 
        self.__estudiantes_facu.append(alumno) 
    
    def contratar_profesor(self, profe:Profesor): 
        self.__profes_facu.append(profe) #Aquí, la instancia de Profesor (profe) se añade a una lista de profesores 
        #de la facultad. La facultad "tiene" a este profesor.

        if self.__cursos: 
            indice_cursos = randint(0,len(self.__cursos)-1)
            profe.set_cursos(self.__cursos[indice_cursos])
            self.__cursos[indice_cursos].set_catedra(profe)
            for departamento in self.__departamentos:
                if departamento.get_nombre_dpt() == self.__cursos[indice_cursos].get_nombre_dpt():
                    profe.set_departamentos(departamento)
                    departamento.set_profes(profe)
                    break
            #Si la facultad fuera eliminada, el objeto Profesor (profe) seguiría existiendo y podría ser "contratado" 
            #por otra facultad o ser una entidad independiente en el sistema.

            
    def crear_departamento(self, nombre_dpto, director: Profesor): # Crear un departamento 
        #con un director
        # Se asume que el director ya es un profesor de la facultad.
        dpto = Departamento(director, nombre_dpto) 
        self.__departamentos.append(dpto)
        director.set_dptm_director(dpto)
        director.set_es_director()  # marca al profesor como director

    
    def inscribir_estudiante_a_curso(self, opcion_del_estudiante, opcion_curso):
        alumno = self.__estudiantes_facu[opcion_del_estudiante]
        self.__cursos[opcion_curso].set_inscriptos(alumno) 
        self.__estudiantes_facu[opcion_del_estudiante].set_cursos_asistidos(self.__cursos[opcion_curso])

    def crear_curso(self, nombre, depto_index, profesor_index):
        departamento = self.departamentos[depto_index]
        profesor = self.professores[profesor_index]
        nuevo_curso = Curso(nombre, departamento, profesor)
        self.cursos.append(nuevo_curso)  # Asegúrate de agregarlo aquí
        departamento.agregar_curso(nuevo_curso)  

    def set_cursos(self, curso:Curso):
        self.__cursos.append(curso)

    def hay_profesores_disponibles(self):
        '''Retorna True si hay al menos un profesor que NO es director.
        Esta función es más clara para la lógica de la opción 3.'''
        for profesor in self.__profes_facu:
            if not profesor.get_es_director():
                return True
        return False
    
    def obtener_profesores_disponibles(self):
        '''Retorna una lista de objetos Profesor que aún no son directores.'''
        return [p for p in self.__profes_facu if not p.get_es_director()]
    
    def obtener_profesores(self):
        '''Retorna la lista completa de objetos Profesor.'''
        return self.__profes_facu

    def obtener_departamentos(self):
        '''Retorna la lista completa de objetos Departamento.'''
        return self.__departamentos
    
    
    def cant_profesores(self):
        return len(self.__profes_facu)
    
    def cant_departamentos(self):
        return len(self.__departamentos)
    
    def cant_cursos(self):
        return len(self.__cursos)
    
    def cant_estudiantes(self):
        return len(self.__estudiantes_facu)

    def mostrar_cursos_asociados(self, num_departamento):
        info_cursos = "El departamento " + str(self.__departamentos[num_departamento].get_nombre_dpt()) + " contiene los siguientes cursos:\n" + str(self.__departamentos[num_departamento].get_nombre_cursos())
        return info_cursos

    def mostrar_profesores(self):
        info_profesores = ""
        i = 1
        for profesor in self.__profes_facu:
            info_profesores += f"{i} - {profesor.get_info()}\n"
            i += 1
        return info_profesores

    def mostrar_alumnos(self):
        info_alumnos = ""
        i = 1
        for estudiante in self.__estudiantes_facu:
            info_alumnos += f"{i} - {estudiante.get_info()}\n"
            i += 1
        return info_alumnos

    def mostrar_departamentos(self):
        info_departamentos = ""
        i = 1
        for departamento in self.__departamentos:
            info_departamentos += f"{i} - {departamento.get_nombre_dpt()}\n"
            i += 1
        return info_departamentos

    def mostrar_cursos(self):
        info_cursos = ""
        i = 1
        for curso in self.__cursos:
            info_cursos += f"{i} - {curso.get_nombre()}\n"
            i += 1
        return info_cursos
    
    def obtener_estudiantes(self):
        '''Retorna la lista completa de objetos Estudiante.'''
        return self.__estudiantes_facu

    def obtener_cursos(self):
        '''Retorna la lista completa de objetos Curso.'''
        return self.__cursos
