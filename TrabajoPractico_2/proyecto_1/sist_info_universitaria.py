from modules.facultad import Facultad
from modules.estudiante import Estudiante
from modules.profesor import Profesor
from random import *
from modules.departamento import Departamento
from modules.curso import Curso


def guardar_archivo(nombre_archivo, facultad):
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
            director_nombre = departamento.get_director()  # ahora es solo string
            archivo.write(f"Departamento: {departamento.get_nombre_dpt()} (Director: {director_nombre})\n")

        # Guardar cursos
        for curso in facultad.obtener_cursos():
            profesor = curso.get_profesor()
            archivo.write(f"Curso: {curso.get_nombre()} (Profesor: {profesor.get_nombre()})\n")



def leer_archivo(nombre_archivo):
    """
    Lee un archivo de texto con datos de una facultad y construye
    los objetos correspondientes.
    Retorna una instancia de Facultad.
    """
    # Inicializar las listas que contendrán los datos
    profesores = []
    alumnos = []
    departamentos_data = []

    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                
                if not linea:  # Ignorar líneas vacías
                    continue

                # LÓGICA DE PROCESAMIENTO ROBUSTA
                try:
                    # 1. LÍNEAS DE PROFESOR
                    if "Profesor" in linea:
                        partes = linea.split(' ')
                        nombre = partes[0]
                        edad = int(partes[1].replace(',', ''))
                        profe = Profesor(nombre, edad)
                        profesores.append(profe)
                    
                    # 2. LÍNEAS DE ESTUDIANTE
                    elif len(linea.split(' ')) == 2 and not linea.startswith("Departamento:") and not linea.startswith("Curso:"):
                        partes = linea.split(' ')
                        nombre = partes[0]
                        edad = int(partes[1].replace(',', ''))
                        estudiante = Estudiante(nombre, edad)
                        alumnos.append(estudiante)

                    # 3. LÍNEAS DE DEPARTAMENTO
                    elif linea.startswith("Departamento:"):
                        partes = linea.split("(Director:")
                        nombre_depto = partes[0].replace("Departamento:", "").strip()
                        director_nombre = partes[1].replace(")", "").strip()
                        departamentos_data.append({'nombre': nombre_depto, 'director': director_nombre})
                    
                    # 4. LÍNEAS DE CURSO
                    elif linea.startswith("Curso:"):
                        # Simplemente imprime un mensaje porque no hay una clase 'Curso'
                        # para instanciar en este momento.
                        print(f"Línea de curso encontrada: {linea}")

                except (ValueError, IndexError) as e:
                    print(f"Advertencia: No se pudo procesar la línea '{linea}'. Error: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return None

    # CONSTRUIR LOS OBJETOS DESPUÉS DE PROCESAR TODO EL ARCHIVO
    if not profesores:
        print("Error: No se encontraron profesores en el archivo. No se puede crear la Facultad.")
        return None

    # Crear la instancia de Facultad. Asume el primer departamento o un director por defecto.
    director_principal = profesores[0]
    facultad = Facultad("Facultad", director_principal)

    # Contratar a todos los profesores
    for prof in profesores:
        facultad.contratar_profesor(prof)

    # Crear los departamentos y asignar directores
    for depto_info in departamentos_data:
        director_obj = next((p for p in profesores if p.get_nombre() == depto_info['director']), None)
        if director_obj:
            facultad.crear_departamento(depto_info['nombre'], director_obj)
        else:
            print(f"Advertencia: Director '{depto_info['director']}' no encontrado.")
    
    # Inscribir a los alumnos
    for alumno in alumnos:
        facultad.inscribir_alumno(alumno)

    return facultad

    print("BIENVENIDO A LA FACULTAD DE INGENIERIA")
    facultad = leer_archivo("archivo.txt")

    if facultad:
        print("---")
        print("Profesores:\n" + facultad.mostrar_profesores())
        print("---")
        print("Alumnos:\n" + facultad.mostrar_alumnos())
        print("---")
    else:
        print("No se pudo iniciar el programa debido a errores en la lectura del archivo.")

facultad = leer_archivo("archivo.txt") #Creamos una copia, llama a la función para crear y poblar la instancia de Facultad.
print("BIENVENIDO A LA FACULTAD DE INGENIERIA \n")
print("Profesores:\n" + facultad.mostrar_profesores())
print('\n\n')
print("Estudiantes:\n" + facultad.mostrar_alumnos())
print('\n\n')
print("Departamentos existentes:\n" + facultad.mostrar_departamentos())
print('\n\n')
print("Cursos existentes:\n" + facultad.mostrar_cursos())

 
def mostrar_menu():
    '''Nuestro menu interactivo'''
    print('\n\n')
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
        edad = int(input("Ingrese la edad del alumno: "))
        if edad >= 0:  # Verifica si la edad es un número positivo
            break
        
        print("Por favor, ingrese un número válido para la edad.")

    alumno = Estudiante(nombre, edad) 
    #alumnos.append(alumno)
    facultad.inscribir_alumno(alumno) #Crea un objeto Estudiante y lo añade tanto a la lista global alumnos como a la facultad usando facultad.inscribir_alumno()
    print(facultad.mostrar_alumnos())

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)
                    
def opcion_2():
    print("Ingrese nombre del profesor: ")
    nombre = input()
    edad = None
    while True:
        edad = int(input("Ingrese la edad del profesor: "))
        if edad >= 0:  # Verifica si la edad es un número positivo
            break
        print("Por favor, ingrese un número válido para la edad.")

    profesor = Profesor(nombre, edad) 
    #profesores.append(profesor)
    facultad.contratar_profesor(profesor)
  
    print(facultad.mostrar_profesores())

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)


def opcion_3():
    # Verifica si hay profesores disponibles para ser directores
    if facultad.hay_profesores_disponibles(): # Necesito un método en tu clase Facultad que liste los profesores sin departamento/director
        print("Ingrese nombre del departamento:")
        nombre_depto = input()
        
        # Muestra los profesores disponibles para ser directores
        print("Profesores disponibles para ser directores:")
        profesores_disponibles = facultad.obtener_profesores_disponibles() # Otro método que necesitarás en la clase Facultad
        for i, profesor in enumerate(profesores_disponibles):
            print(f"{i+1}. {profesor.get_nombre ()}")

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
    else:
        print("No hay profesores disponibles para ser directores. Se sugiere contratar un nuevo profesor.")

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)
        
def opcion_4():
    #Muestra los departamentos existentes y pide al usuario que seleccione uno por número. 
    #Valida que el número esté dentro del rango.

    #Muestra los profesores existentes y pide al usuario que seleccione uno por número para 
    #que enseñe en el curso. Valida el número.

    while True:  # Bucle para solicitar la entrada del usuario hasta que se proporcione un valor válido
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

            print(facultad.mostrar_cursos_asociados(opcion - 1))
            

            break  # Salir del bucle si todo está correcto
        except ValueError as e:  # Capturar excepciones de tipo ValueError
            print("Por favor, ingrese un número válido.\n")

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)
 
def opcion_5():
    while True:  # Bucle para solicitar la entrada del usuario hasta que se proporcione un valor válido
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
            
            cursos_inscritos_indices = []  # Lista para mantener los índices de los cursos inscritos
            while cant_cursos > 0: #Muestra la lista de cursos disponibles y pide al usuario que seleccione uno.
                print(facultad.mostrar_cursos() + "Seleccione la opcion: \n") 
                opcion_curso = int(input())
                if opcion_curso < 1 or opcion_curso > facultad.cant_cursos(): 
                    raise ValueError("Número de curso fuera de rango")
                
                # Verificar si la opción seleccionada coincide con algún índice ya elegido
                if opcion_curso - 1 in cursos_inscritos_indices: #evita que el mismo alumno sea inscrito dos veces en el mismo curso.
                    print("El alumno ya está inscrito en ese curso. Por favor, seleccione otro curso.")
                else:
                    # Inscribir al alumno en el curso y agregar el índice a la lista de índices inscritos
                    facultad.inscribir_estudiante_a_curso(opcion_estudiante-1, opcion_curso - 1)
                    cursos_inscritos_indices.append(opcion_curso - 1)
                    cant_cursos -= 1

            print("Alumnos: \n" + facultad.mostrar_alumnos())
            print('\n\n')
            
            break  # Salir del bucle si todo está correcto
        except ValueError as e:  # Capturar excepciones de tipo ValueError
            print("Por favor, ingrese un número válido.\n")  

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)

def opcion_6():
    print("Seleccionaste la Opción 6")

    # Guardar cambios en el archivo
    guardar_archivo("archivo.txt", facultad)

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
        break
    else:
        print("Opción no válida. Por favor, ingrese un número válido.")
