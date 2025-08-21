from datetime import datetime
from random import *
import os
import matplotlib
matplotlib.use('Agg') # Le dice a Matplotlib que use un backend no interactivo, diseñado específicamente 
# para generar imágenes directamente en archivos (como PNGs, JPGs o PDFs), sin intentar abrir 
# una ventana gráfica o interactuar con una interfaz de usuario (GUI).

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Define el nombre de los archivos.
archivo_frases='frases_de_peliculas.txt' 
archivo_partidas='datos_partidas.txt'
#------------------------------------------------------------------------#OBTENCION DE DATOS

def fecha_hora():
    '''Funcion que retorna la fecha y la hora actual en formato dd/mm/aa'''
    ahora = datetime.now()
    # Formatea la fecha y hora en la cadena deseada
    fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S') 
    return fecha_y_hora

def obtener_puntuacion(aciertos, intentos): 
    '''Funcion que retorna la puntuacion de la forma: Aciertos/IntentosTotales (String)'''  
    return str(aciertos) + "/" + str(intentos) #Concatena los valores numéricos aciertos e intentos con un / en el medio.

def guardar_fecha_hora(ruta_base):
    '''Funcion que guarda la fecha y la hora actual en el archivo'''
    ruta_archivo = os.path.join(ruta_base, archivo_partidas)
    with open(ruta_archivo, 'a') as archivo:
        # Añade un espacio después de la fecha y hora
        archivo.write(fecha_hora() + " ") 

def guardar_nombre(nombre, ruta_base):
    '''Funcion que guarda el nombre del jugador en el archivo'''
    ruta_archivo = os.path.join(ruta_base, archivo_partidas)
    with open(ruta_archivo, 'a') as archivo:
        # Añade un espacio después del nombre
        archivo.write(nombre + " ")

def guardar_intentos(intentos, ruta_base):
    '''Funcion que guarda el numero de intentos totales en el archivo'''
    ruta_archivo = os.path.join(ruta_base, archivo_partidas)
    with open(ruta_archivo, 'a') as archivo:
        # Añade un espacio después de los intentos
        archivo.write(str(intentos) + " ")

def guardar_puntuacion(puntuacion, ruta_base):
    '''
    Funcion que guarda la puntuacion final en el archivo.
    Se añade un salto de línea para separar las partidas.
    '''
    ruta_archivo = os.path.join(ruta_base, archivo_partidas)
    with open(ruta_archivo, 'a') as archivo:
        # Añade un salto de línea al final de la puntuación
        archivo.write(puntuacion + "\n") 


#----------------------------------------------------------------------#MANEJO DE ARCHIVOS Y LISTAS

def leer_archivo(nombre_archivo, ruta_base):
    """
    Lee y retorna el contenido completo del archivo.
    Acepta el nombre del archivo y la ruta base del proyecto.
    """
    ruta_archivo = os.path.join(ruta_base, nombre_archivo)
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
        return texto
    except FileNotFoundError:
        # Genera una excepción detallada para facilitar la depuración
        raise Exception(f"Error: El archivo '{nombre_archivo}' no se encontró en la ruta: {ruta_archivo}. Por favor, verifica su ubicación.")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado al leer el archivo '{nombre_archivo}': {e}")
    
def escribir_archivo(nombre_archivo,lista): 
    '''Funcion generica que escribe archivos de texto en base a una lista de python,
    recibe como parametro el nombre del archivo y la lista de elementos a escribir'''
    archivo = open(nombre_archivo,'w')
    i = 0
    while i < len(lista) :
        archivo.write(lista[i] + '\n') #Itera sobre la lista y escribe cada elemento seguido de un salto de línea.
        i = i + 1

    archivo.close()
    
def generar_listado_peliculas(par_texto): 
    '''Funcion que recibe un string con el contenido del archivo "frases_de_peliculas.txt" y retorna una lista con las peliculas'''
    peliculas = []
    
    lineas = par_texto.strip().split('\n')
    for linea in lineas:
        partes = linea.split(';')
        if len(partes) > 1:
            pelicula = partes[1].strip()
            peliculas.append(pelicula)
    return peliculas

def generar_listado_frases(par_texto): 
      '''Funcion que recibe un string con el contenido del archivo "frases_de_peliculas.txt" y 
          retorna una lista con las frases'''
      frases = []
      lineas = par_texto.strip().split('\n')
      for linea in lineas:
          partes = linea.split(';')
          if len(partes) > 0:
              frase = partes[0].strip()
              frases.append(frase)
      return frases
  
def acomodar_lista(lista): 
    '''Funcion que recibe la lista de las peliculas, las convierte a minusculas y elimina las repetidas, retorna una lista ordenada'''
    lista = [cadena.lower() for cadena in lista]
    lista = list(set(lista)) #Eliminar elementos duplicados
    lista.sort() #Ordenar alfabéticamente la lista
    return lista
      
def generar_archivo_frases(par_texto): #Crea un archivo llamado frases.txt y escribe en él todas las frases obtenidas del par_texto.
      '''Generamos un archivo .txt con las frases de las peliculas'''
      return escribir_archivo('frases.txt',generar_listado_frases(par_texto))
      
def generar_opciones(ruta_base): 
    '''Genera las opciones de peliculas y la frase, retorna una lista con 5 elementos:
    las tres peliculas, la frase a jugar y el indice de esa frase'''
    text = leer_archivo(archivo_frases, ruta_base) # Aquí se llama a la función de forma correcta
    
    # Si el archivo no se pudo leer, la función leer_archivo ya devuelve una cadena de error
    if not text:
        return []
    
    pelis = generar_listado_peliculas(text)
    frases = generar_listado_frases(text)
    opc_peli = []

    # Verificar si la lista de frases está vacía antes de continuar
    if not frases:
        # Si la lista de frases está vacía, retornar una lista vacía para evitar el ValueError
        return []

    indice_frase = randint(0,len(frases)-1) #Selecciona una frase al azar y su película correcta.
    opc_peli.append(pelis[indice_frase].lower()) #Añade la película correcta
    pelis = acomodar_lista(pelis) #Limpia y ordena la lista completa de películas

    while len(opc_peli) < 3: 
        #Selecciona dos películas aleatorias y únicas de la lista limpia que no 
        #sean la correcta, añadiéndolas a opc_peli.
        indice_pelicula = randint(0,len(pelis)-1)
        pelicula_elegida = pelis[indice_pelicula]
        if pelicula_elegida not in opc_peli:
            opc_peli.append(pelicula_elegida)

    shuffle(opc_peli) #hacemos que las pelis se distribuyan aleatoriamente en el vector para las opciones 
    opc_peli.append(frases[indice_frase]) #ubicamos la frase en la ante ultima posicion
    opc_peli.append(indice_frase) #guardo el indice de la frase en la ultima posicion
    return opc_peli

def listar_fechas(archivo, ruta_base): 
    '''Lee las fechas del archivo datos_partidas.txt y retorna una lista con las fechas en las que se ha jugado a la trivia'''
    ruta_archivo = os.path.join(ruta_base, archivo)
    
    if not os.path.exists(ruta_archivo):
        return []

    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    fechas = []
    for linea in lineas:
        fecha = linea[:10]
        if fecha not in fechas:
            fechas.append(fecha)
    return fechas

def acumular_aciertos(archivo, fechas, ruta_base): 
    '''Acumulo los aciertos de todos los jugadores para una fecha en particular, recibe el archivo con los datos
    de las partidas jugadas y la lista de las fechas en las que se ha jugado a la trivia.
    Retorna una lista con los aciertos acumulados para cada fecha en la que se ha jugado a la trivia'''
    aciertos = [0] * len(fechas)
    ruta_archivo = os.path.join(ruta_base, archivo)

    if not os.path.exists(ruta_archivo):
        return aciertos

    with open(ruta_archivo, 'r') as file:
        lineas = file.readlines()
        for linea in lineas:
            partes = linea.split()
            if len(partes) < 5:
                continue
            
            fecha = partes[0]
            # Se extrae el número de aciertos de la puntuación (ej. '5/10')
            acierto_val = int(partes[4].split('/')[0])
            
            
            if fecha in fechas:
                aciertos[fechas.index(fecha)] += acierto_val

    return aciertos

def acumular_desaciertos(archivo, fechas, aciertos, ruta_base): 
    '''Acumulo los desaciertos de todos para una fecha en particular, recibe el archivo con los datos
    de las partidas jugadas, la lista de las fechas en las que se ha jugado a la trivia, y la lista de los
    aciertos acumulados para cada fecha en la que se ha jugado a la trivia.
    Retorna una lista con los desaciertos acumulados para cada fecha.
    '''
    intentos = [0] * len(fechas)
    desaciertos = []
    ruta_archivo = os.path.join(ruta_base, archivo)

    if not os.path.exists(ruta_archivo):
        return [0] * len(fechas)

    with open(ruta_archivo, 'r') as file:
        lineas = file.readlines()
        for linea in lineas:
            partes = linea.split()
            if len(partes) < 5:
                continue

            fecha = partes[0]
            intento = partes[4].split('/')
            intento_val = int(intento[1])
            
            if fecha in fechas:
                intentos[fechas.index(fecha)] += intento_val
    
    i = 0
    while i < len(aciertos):
        desaciertos.append( intentos[i] - aciertos[i] )
        i += 1
    return desaciertos

#----------------------------------------------------------------------------------#GRAFICACION
def crear_figura_eje_coordenado(ruta_base):
    archivo_docs = "datos_partidas.txt"
    lista_fechas = listar_fechas(archivo_docs, ruta_base)
    lista_aciertos_acumulados = acumular_aciertos(archivo_docs, lista_fechas, ruta_base)
    lista_desaciertos_acumulados = acumular_desaciertos(archivo_docs, lista_fechas, lista_aciertos_acumulados, ruta_base)
    
    fig = plt.figure(figsize=(10, 5))
    plt.plot(lista_fechas, lista_aciertos_acumulados, label='Aciertos')
    plt.plot(lista_fechas, lista_desaciertos_acumulados, label='Desaciertos')
    plt.xlabel('Fechas')
    plt.ylabel('Aciertos/Desaciertos')
    plt.title('Gráficas de aciertos/desaciertos vs Fechas del intento')
    plt.grid(True)
    plt.legend()
    return fig

def crear_figura_circular(ruta_base):
    archivo_docs = "datos_partidas.txt"
    lista_fechas = listar_fechas(archivo_docs, ruta_base)
    lista_aciertos_acumulados = acumular_aciertos(archivo_docs, lista_fechas, ruta_base)
    lista_desaciertos_acumulados = acumular_desaciertos(archivo_docs, lista_fechas, lista_aciertos_acumulados, ruta_base)

    labels = ['Aciertos', 'Desaciertos']
    sizes = [sum(lista_aciertos_acumulados), sum(lista_desaciertos_acumulados)]
    colors = ['lightblue', 'lightcoral']
    
    fig = plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Proporción de Aciertos y Desaciertos')
    return fig

def generar_graficas_para_html(path_base_app):
    fig_ejes = crear_figura_eje_coordenado(path_base_app)
    ruta_static = os.path.join(path_base_app, 'static')
    os.makedirs(ruta_static, exist_ok=True)
    ruta_guardado_ejes = os.path.join(ruta_static, 'grafica_ejes.png')
    fig_ejes.savefig(ruta_guardado_ejes)
    plt.close(fig_ejes)

    fig_circular = crear_figura_circular(path_base_app)
    ruta_guardado_circular = os.path.join(ruta_static, 'grafico_circular.png')
    fig_circular.savefig(ruta_guardado_circular)
    plt.close(fig_circular)

if __name__ == "__main__":
    pass