from flask import render_template, request,send_file, session 
from modules.config import app

# Importa tus funciones actualizadas desde modules.funciones
from modules.funciones import * # Importa las funciones principales de Flask:
# send_file: Para enviar archivos al navegador del usuario, como tu PDF

from matplotlib.backends.backend_pdf import PdfPages
import io
import os
import matplotlib.pyplot as plt

'''@app.route("URL asociada (Nombre .html)", Metodos GET/POST para enviar o recibir solicitudes del formulario), es un decorador'''

'''return render_template() : render_template(): Función de Flask que se utiliza para 
renderizar una plantilla HTML. Toma al menos un argumento, 
que es el nombre del archivo de la plantilla (por ejemplo, "inicio.html").
Puedes pasar más argumentos a render_template() para proporcionar 
datos dinámicos a la plantilla. En esto caso variables Python'''

'''request.form=request.form es un 'diccionario-like object' en Flask que contiene los datos enviados 
desde un formulario HTML usando el método POST. Cuando un formulario HTML es enviado usando POST, 
los datos del formulario son enviados al servidor y pueden ser accesados en Flask usando request.form.'''

lista_frase_id = [] # lista para almacenar los id de las frases jugadas, para evitar que se
#                   repitan en un mismo juego

# Configuración de la sesión para el nombre de usuario
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_secreta' # Es necesario para usar la sesión


# Las rutas son las direcciones URL a las que tu aplicación responde. 
# Cada función decorada con @app.route(...) maneja una URL específica.


@app.route("/", methods = ["GET", "POST"]) 
def inicio(): 
    '''Renderiza a la pagina de inicio, inicio.html'''
    return render_template("inicio.html")
# La función inicio() se ejecuta cuando un usuario accede a la URL raíz ("/") de tu aplicación.

#render_template() es una función que Flask proporciona. Su trabajo es tomar un archivo de 
#plantilla HTML (en este caso, "inicio.html") y procesarlo.

@app.route("/juego",methods = ["GET", "POST"])
def juego(): 
    '''Renderiza a la pagina del juego, juego.html, haciendo uso de las variables necesarias obtenidas a partir
    de funciones implementadas en funciones.py e informacion recibida desde el formulario'''
    # Se genera una lista de peliculas aleatorias y se selecciona una frase aleatoria
    pelis_aleatorias = generar_opciones(app.root_path)
    
    if not pelis_aleatorias:
      return render_template("juego.html", mensaje="No se encontraron frases de películas. Por favor, asegúrate de que el archivo 'frases_de_peliculas.txt' no esté vacío y tenga el formato correcto.")
    
    while pelis_aleatorias[4] in lista_frase_id: #control de que sea una frase diferente en cada intento
      pelis_aleatorias = generar_opciones(app.root_path)
      

    frase_aleatoria = pelis_aleatorias[3] #frase aleatoria es la frase que se va a jugar
    indice_correcto = pelis_aleatorias[4]
    num_int = request.form ['intentos_restantes']
    intentos_totales = int(num_int)
    aciertos = 0
    
    # Si se recibe un nombre desde el formulario, lo guarda en la sesión
    if "input_nombre" in request.form:
        nombre = request.form['input_nombre']
        session['nombre_jugador'] = nombre
        lista_frase_id.clear() # Limpia la lista de frases para una nueva partida

    lista_frase_id.append(pelis_aleatorias[4]) #guardo el id de la frase jugada

    if "aciertos" in request.form:  
        aciertos = int(request.form['aciertos'])
        intentos_totales = int(request.form['intentos_totales'])

    
    return render_template("juego.html", 
                           intentos_totales = intentos_totales,
                           peli_1 = pelis_aleatorias[0], 
                           peli_2 = pelis_aleatorias[1],
                           peli_3 = pelis_aleatorias[2], 
                           frase = frase_aleatoria, 
                           aciertos = aciertos, 
                           indice = indice_correcto,
                           intentos_restantes = num_int,)
                
                           

@app.route('/juego/comprobar_opcion', methods = ["GET", "POST"])
def comprobar_opcion(): 
    '''Funcion que realiza controles para determinar si la opcion seleccionada por el usuario es correcta o incorrecta.
    En base a lo anterior determina si los botones en la pagina juego.html: "Continuar" y "Ver resultado" se habilitan.
    Al finalizar renderiza a la pagina de juego, juego.html, con la informacion correspondiente a ese intento o frase jugada'''
                 
    opcion_del_usuario = request.form['boton']
    indice_correcto = int(request.form['indice_correcto'])
    num_int = int(request.form['intentos_restantes']) - 1
    aciertos = int(request.form['aciertos'])     # con request.form tomamos las variables que necesitemos del servidor (POST)
    peli_1 =  request.form['peli_1']
    peli_2 = request.form['peli_2']
    peli_3 = request.form['peli_3'] 
    frase = request.form['frase']
    intentos_totales = int(request.form['intentos_totales'])
    
    
    # Obtiene el nombre del jugador de la sesión
    nombre = session.get('nombre_jugador', 'Jugador')  
    
    texto = leer_archivo('frases_de_peliculas.txt', app.root_path)
    pelis = generar_listado_peliculas(texto)     
    respuesta_correcta = pelis[indice_correcto].lower()

    if opcion_del_usuario == respuesta_correcta: 
        mensaje = "¡Correcto! ¡Respuesta correcta!"
        aciertos = aciertos + 1
    else:
        mensaje = "Incorrecto. La respuesta correcta es: " + respuesta_correcta

    if 0 < num_int: # control para aparicion de los botones "continuar" y "ver resultado"
        habilitar_continuar = True
        habilitar_ver_res = False
    else:
        habilitar_continuar = False
        # Las funciones individuales se llaman en el orden correcto
        guardar_fecha_hora(app.root_path)
        guardar_nombre(nombre, app.root_path)
        guardar_intentos(intentos_totales, app.root_path)
        guardar_puntuacion(obtener_puntuacion(aciertos, intentos_totales), app.root_path)
        habilitar_ver_res = True
        # Se guarda la puntuacion en el archivo de texto "datos_partidas.txt"
        

    return render_template("juego.html",   # le fuimos pasando a juego lo que vimos necesario
                           intentos_totales = intentos_totales , 
                           mensaje = mensaje,
                           peli_1 = peli_1,
                           peli_2 = peli_2,
                           peli_3 = peli_3,
                           frase = frase,
                           opcion_seleccionada = opcion_del_usuario,
                           intentos_restantes = num_int, 
                           habilitar_continuar = habilitar_continuar, 
                           aciertos = aciertos, 
                           habilitar_ver_res = habilitar_ver_res,
                           indice = indice_correcto)
                           
@app.route("/final_del_juego",methods = ["GET", "POST"])
def final_del_juego(): 
    '''Renderiza a la pagina final_del_juego.html, enviando al formulario la puntuacion obtenida'''
    aciertos = int(request.form['aciertos'])
    intentos = int(request.form['intentos_totales'])
    puntuacion = obtener_puntuacion(aciertos, intentos)
    return render_template("final_del_juego.html", puntuacion = puntuacion)

@app.route("/resultados", methods = ["GET", "POST"])
def resultados_juego():
    '''Renderiza a resultados.html, envia al formulario la informacion recopilada en el archivo de texto "datos_partidas.txt"'''
    texto = leer_archivo("datos_partidas.txt", app.root_path)
    
    return render_template("resultados.html", texto = texto)


@app.route("/graficas", methods = ["GET", "POST"])
def graficas_juego():
    '''Se realizan llamados a las funciones encargadas de crear las graficas y guardarlas en archivos .png'''
    generar_graficas_para_html(app.root_path) # Llama a la nueva función que guarda PNGs
    return render_template("graficas.html")

@app.route('/generar_archivo_pdf', methods = ["GET", "POST"])
def generar_archivo_pdf():
    '''Genera un archivo PDF con las graficas de los resultados del juego y lo envía al usuario.'''
    # Asegúrate de que las funciones crear_figura_eje_coordenado y crear_figura_circular
    # estén definidas en modules.funciones y retornen las figuras correspondientes.
    try:
        with io.BytesIO() as buffer:
            with PdfPages(buffer) as pdf:
                # Llama a las funciones que RETORNAN las figuras
                fig_ejes = crear_figura_eje_coordenado(app.root_path)
                pdf.savefig(fig_ejes) # Guarda la figura retornada en el PDF
                plt.close(fig_ejes) # Cierra la figura después de guardarla en el PDF

                fig_circular = crear_figura_circular(app.root_path)
                pdf.savefig(fig_circular) # Guarda la figura retornada en el PDF
                plt.close(fig_circular) # Cierra la figura después de guardarla en el PDF

            buffer.seek(0)
            
            # Asegúrate de que la carpeta 'docs' exista dentro de 'proyecto_1'
            ruta_pdf_destino_dir = os.path.join(app.root_path, 'docs')
            os.makedirs(ruta_pdf_destino_dir, exist_ok=True) # Crea la carpeta 'docs' si no existe

            ruta_pdf_destino_file = os.path.join(ruta_pdf_destino_dir, 'graficas_resultados.pdf') 
            
            with open(ruta_pdf_destino_file, "wb") as file:
                file.write(buffer.getvalue())
        
        # Envía el archivo PDF generado
        return send_file(ruta_pdf_destino_file, as_attachment=True, download_name='graficas_resultados.pdf')

    except Exception as e:
        # En caso de cualquier error durante la generación del PDF
        return f"Error al generar el PDF: {e}", 500

@app.route("/listado_pelis", methods = ["GET", "POST"]) 
def listado_peliculas():
    '''Renderiza listado_pelis.html, enviando al formulario el listado de las peliculas indexadas, ordenadas y filtradas
    segun las exigencias del enunciado'''
    texto = leer_archivo("frases_de_peliculas.txt", app.root_path)
    lista = generar_listado_peliculas(texto)
    lista = acomodar_lista(lista)
    i = 0
    for pelicula in lista:
        lista[i] = str(i+1) + ") " + pelicula
        i += 1

    return render_template("listado_pelis.html", lista = lista) 


if __name__ == "__main__":
    app.run(debug = True)