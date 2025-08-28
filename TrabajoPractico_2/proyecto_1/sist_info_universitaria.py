from modules.facultad import Facultad
from modules.estudiante import Estudiante
from modules.profesor import Profesor
from random import *
from modules.departamento import Departamento
from modules.curso import Curso


def guardar_archivo(nombre_archivo, facultad):
    """
    Guarda los datos de la facultad en un archivo de texto.
    """
    with open(nombre_archivo, 'w') as archivo:
        # Guardar profesores
        for profesor in facultad.obtener_profesores():
            archivo.write(f"{profesor.get_nombre()} {profesor.get_edad()}, Profesor\n")

        archivo.write("\n")  # separar con línea vacía

        # Guardar estudiantes
        for estudiante in facultad.obtener_estudiantes():
            archivo.write(f"{estudiante.get_nombre()} {estudiante.get_edad()}\n")

        archivo.write("\n")  # separar con línea vacía

        # Guardar departamentos
        for departamento in facultad.obtener_departamentos():
            director = departamento.get_director()
            director_nombre = director.get_nombre() if isinstance(director, Profesor) else str(director)
            archivo.write(f"Departamento: {departamento.get_nombre_dpt()} (Director: {director_nombre})\n")

        archivo.write("\n")  # separar con línea vacía

        # Guardar cursos
        for curso in facultad.obtener_cursos():
            profesor = curso.get_profesor()
            departamento = curso.get_departamento()
            archivo.write(f"Curso: {curso.get_nombre()} (Departamento: {departamento.get_nombre_dpt()}, Profesor: {profesor.get_nombre()})\n")

def leer_archivo(nombre_archivo):
    '''Funcion que lee el archivo que armamos para la prueba, retorna un objeto del tipo facultad'''
    profesores_str = []
    alumnos_str = []
    departamentos_str = []
    cursos_str = []

    try:
        with open(nombre_archivo, 'r') as archivo:
            # Leer cada línea del archivo y clasificarla
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue

                if "Profesor" in linea:
                    profesores_str.append(linea)
                elif linea.startswith("Departamento:"):
                    departamentos_str.append(linea)
                elif linea.startswith("Curso:"):
                    cursos_str.append(linea)
                else:
                    alumnos_str.append(linea)
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return None

    # CONSTRUIR EL OBJETO FACULTAD CON LOS DATOS LEÍDOS EN EL ORDEN CORRECTO
    profesores = []
    for linea in profesores_str:
        partes = linea.split(',')
        if len(partes) == 2:
            nombre_y_edad = partes[0].strip().rsplit(' ', 1)
            if len(nombre_y_edad) == 2 and nombre_y_edad[1].isdigit():
                nombre = nombre_y_edad[0]
                edad = int(nombre_y_edad[1])
                profe = Profesor(nombre, edad)
                profesores.append(profe)
    if not profesores:
        print("No se encontraron profesores para crear la facultad.")
        # Se crea una facultad por defecto si no hay datos en el archivo.
        director_principal = Profesor("Director Por Defecto", 45)
        objeto_facultad = Facultad("Ingenieria", director_principal)
        return objeto_facultad

    director_principal = profesores[0]
    objeto_facultad = Facultad("Ingenieria", director_principal)

    for profesor in profesores[1:]:
        objeto_facultad.contratar_profesor(profesor)

    # Crear departamentos
    for linea in departamentos_str:
        partes = linea.split("(Director:")
        nombre_depto = partes[0].replace("Departamento:", "").strip()
        director_nombre = partes[1].replace(")", "").strip()
        director = next((p for p in profesores if p.get_nombre() == director_nombre), None)
        if director:
            objeto_facultad.crear_departamento(nombre_depto, director)

    # Crear cursos
    # Se ha actualizado la lógica de lectura para el nuevo formato del archivo
    for linea in cursos_str:
        linea_limpia = linea.replace("Curso: ", "").strip()
        try:
            partes = linea_limpia.split("(Departamento: ")
            nombre_curso = partes[0].strip()
            rest = partes[1].split(", Profesor: ")
            nombre_depto = rest[0].replace(")", "").strip()
            profesor_nombre = rest[1].replace(")", "").strip()

            profesor = next((p for p in profesores if p.get_nombre() == profesor_nombre), None)
            depto = next((d for d in objeto_facultad.obtener_departamentos() if d.get_nombre_dpt() == nombre_depto), None)

            if profesor and depto:
                depto_index = objeto_facultad.obtener_departamentos().index(depto)
                profesor_index = profesores.index(profesor)
                objeto_facultad.crear_curso(nombre_curso, depto_index, profesor_index)
        except IndexError:
            # Manejar el formato antiguo de la línea si no tiene el departamento
            print(f"Advertencia: Formato de línea de curso obsoleto, no se pudo cargar: '{linea}'")

    # Crear alumnos
    for linea in alumnos_str:
        partes = linea.rsplit(' ', 1)
        if len(partes) == 2 and partes[1].isdigit():
            nombre = partes[0]
            edad = int(partes[1])
            estudiante = Estudiante(nombre, edad)
            objeto_facultad.inscribir_alumno(estudiante)

    return objeto_facultad


def mostrar_menu():
    '''Nuestro menu interactivo'''
    print('\n\n')
    print("BIENVENIDO A LA FACULTAD DE INGENIERIA\n")
    print("Profesores:\n" + facultad.mostrar_profesores())
    print("Estudiantes:\n" + facultad.mostrar_alumnos())
    print("Departamentos existentes:\n" + facultad.mostrar_departamentos())
    print("Cursos existentes:\n" + facultad.mostrar_cursos())
    print("1. Inscribir Alumno")
    print("2. Contratar Profesor")
    print("3. Crear Departamento Nuevo")
    print("4. Crear Curso Nuevo")
    print("5. Inscribir estudiante a un curso")
    print("6. Salir")

def opcion_1():
    print("Ingrese nombre del alumno: ")
    nombre=input()
    edad = None
    while True:
        try:
            edad = int(input("Ingrese la edad del alumno: "))
            if edad >= 0:
                break
            print("Por favor, ingrese un número válido para la edad.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

    alumno = Estudiante(nombre, edad)
    facultad.inscribir_alumno(alumno)
    print(facultad.mostrar_alumnos())
    guardar_archivo("archivo.txt", facultad)

def opcion_2():
    print("Ingrese nombre del profesor: ")
    nombre = input()
    edad = None
    while True:
        try:
            edad = int(input("Ingrese la edad del profesor: "))
            if edad >= 0:
                break
            print("Por favor, ingrese un número válido para la edad.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

    profesor = Profesor(nombre, edad)
    facultad.contratar_profesor(profesor)
    print(facultad.mostrar_profesores())
    guardar_archivo("archivo.txt", facultad)

def opcion_3():
    if not facultad.hay_profesores_disponibles():
        print("No hay profesores disponibles para ser directores. Se sugiere contratar un nuevo profesor.")
    else:
        print("Ingrese nombre del departamento:")
        nombre_depto = input()
        
        print("Profesores disponibles para ser directores:")
        profesores_disponibles = facultad.obtener_profesores_disponibles()
        for i, profesor in enumerate(profesores_disponibles):
            print(f"{i+1}. {profesor.get_nombre()}")

        while True:
            try:
                opcion_director = int(input("Seleccione el número del profesor para ser director: ")) - 1
                if 0 <= opcion_director < len(profesores_disponibles):
                    director_elegido = profesores_disponibles[opcion_director]
                    facultad.crear_departamento(nombre_depto, director_elegido)
                    print(f"Departamento '{nombre_depto}' creado con {director_elegido.get_nombre()} como director.")
                    print("Departamentos existentes:\n" + facultad.mostrar_departamentos())
                    break
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")
    guardar_archivo("archivo.txt", facultad)

def opcion_4():
    while True:
        try:
            print("Ingrese nombre del curso:\n")
            nombre = input()
            
            print("¿De qué departamento formará parte? Ingrese el número correspondiente \n"
                  + facultad.mostrar_departamentos())
            opcion = int(input())
            if opcion < 1 or opcion > facultad.cant_departamentos():
                raise ValueError("Número de departamento fuera de rango")
            
            print("¿Qué profesor enseñará en el curso? Ingrese el número correspondiente \n" + facultad.mostrar_profesores())
            opcion_profesor = int(input())
            if opcion_profesor < 1 or opcion_profesor > facultad.cant_profesores():
                raise ValueError("Número de profesor fuera de rango")
            
            facultad.crear_curso(nombre, opcion - 1, opcion_profesor - 1)
            print(facultad.mostrar_cursos_asociados(opcion - 1))  # Verifica si el curso se añadió
            guardar_archivo("archivo.txt", facultad)  # Asegúrate de que el archivo se guarda correctamente
            break
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente de nuevo.")


def opcion_5():
    while True:
        try:
            print("Alumnos y su condicion actual: \n" + facultad.mostrar_alumnos())
            
            print("Seleccione el numero correspondiente al alumno a inscribir: \n")
            opcion_estudiante = int(input())
            if opcion_estudiante < 1 or opcion_estudiante > facultad.cant_estudiantes():
                raise ValueError("Número de alumno fuera de rango")
            
            print("A cuantos cursos se quiere inscribir el alumno?:\n")
            cant_cursos = int(input())
            if cant_cursos < 1 or cant_cursos > facultad.cant_cursos():
                raise ValueError("Ingrese un valor valido")
            
            cursos_inscritos_indices = []
            while cant_cursos > 0:
                print(facultad.mostrar_cursos() + "Seleccione la opcion: \n")
                opcion_curso = int(input())
                if opcion_curso < 1 or opcion_curso > facultad.cant_cursos():
                    raise ValueError("Número de curso fuera de rango")
                
                if opcion_curso - 1 in cursos_inscritos_indices:
                    print("El alumno ya está inscrito en ese curso. Por favor, seleccione otro curso.")
                else:
                    facultad.inscribir_estudiante_a_curso(opcion_estudiante-1, opcion_curso - 1)
                    cursos_inscritos_indices.append(opcion_curso - 1)
                    cant_cursos -= 1

            print("Alumnos: \n" + facultad.mostrar_alumnos())
            print('\n\n')
            
            break
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente de nuevo.")
    guardar_archivo("archivo.txt", facultad)

def opcion_6():
    print("Seleccionaste la Opción 6")
    guardar_archivo("archivo.txt", facultad)


if __name__ == '__main__':
    facultad = leer_archivo("archivo.txt")
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción que desea seleccionar: \n")

        if opcion == "1":
            opcion_1()
        elif opcion == "2":
            opcion_2()
        elif opcion == "3":
            opcion_3()
        elif opcion == "4":
            opcion_4()
        elif opcion == "5":
            opcion_5()
        elif opcion == "6":
            print("Saliendo del programa...")
            opcion_6()
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

