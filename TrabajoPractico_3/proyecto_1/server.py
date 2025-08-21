from flask import render_template, redirect, url_for, flash, abort, session, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user                                                                  #pip install email-validator
from functools import wraps
from fpdf import FPDF
import textwrap
import base64
import warnings

#esto es para limpiar los warnings de sklearn
from flask import render_template, redirect, url_for, flash, abort, session, request, make_response
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

from modules.forms import LoginForm, RegisterForm
from modules.config import app, login_manager, db
from modules.gestor_reclamos import GestorReclamo
from modules.gestor_usuario import GestorUsuario
from modules.gestor_db import GestorDB
from modules.monticulo_mediana import MonticuloMediana
from modules.gestor_db import GestorDB
from modules.reclamo import Reclamo



with app.app_context():
    # Inicializamos los gestores de base de datos y usuario
    # y cargamos los administradores desde el archivo 'administradores.txt'
    gestor_db = GestorDB(db)
    gestor_usuario = GestorUsuario(gestor_db)
    admin_info = gestor_usuario.cargar_administradores('administradores.txt')
    gestor_reclamo = GestorReclamo(gestor_db)
    cant_reclamos_proceso = gestor_reclamo.dias_segun_estado('en proceso')
    cant_reclamos_resueltos = gestor_reclamo.dias_segun_estado('resuelto')

mediana_proceso = MonticuloMediana()
mediana_resuelto = MonticuloMediana()

mediana_resuelto.calcular_mediana(cant_reclamos_resueltos)
mediana_proceso.calcular_mediana(cant_reclamos_proceso)

#  admin_info es una lista de tuplas (id,departamento)
admin_list = [admin[0] for admin in admin_info]
admin_list = [int(admin_id) for admin_id in admin_list]

with app.app_context(): # Para la corrección 
    encripted_pass = generate_password_hash(password= "12345", method= 'pbkdf2:sha256',salt_length=8) 
    gestor_usuario.crear_cliente("Nikola", "Tesla", encripted_pass, "NTesla", "Estudiante", "teslanikola@hotmail.com")
    gestor_usuario.crear_cliente("Marie", "Curie", encripted_pass, "MCurie", "Docente", "curiemarie@hotmail.com")
    cliente_1 = gestor_usuario.consultar_usuario('email','teslanikola@hotmail.com')
    cliente_2 = gestor_usuario.consultar_usuario('email','curiemarie@hotmail.com')
   
    reclamo_1_1 = gestor_reclamo.crear_reclamo("Solicito que se realice una revisión de las luces en los pasillos del modulo 3, ya que algunas están parpadeando y otras no funcionan, lo que dificulta la visibilidad durante la noche.")
    reclamo_1_2 = gestor_reclamo.crear_reclamo("Reporto que la computadora de la sala de computación está muy lenta y a veces se congela, dificultando mi trabajo en clase. ¿Podrían revisarla y solucionar este problema?")
    reclamo_2_1 = gestor_reclamo.crear_reclamo("Deseo informar sobre una falla en la infraestructura de mi aula, específicamente con el sistema de iluminación. ¿Pueden enviar a alguien a revisar y solucionar este problema?")
    reclamo_2_2 = gestor_reclamo.crear_reclamo("Quisiera solicitar la limpieza profunda de las pizarras en las aulas del modulo 1, ya que presentan manchas difíciles de borrar que dificultan la visibilidad de los apuntes.")

    gestor_reclamo.guardar_reclamo(reclamo_1_1 , cliente_1.get_id())
    gestor_reclamo.guardar_reclamo(reclamo_1_2 , cliente_1.get_id())
    gestor_reclamo.guardar_reclamo(reclamo_2_1 , cliente_2.get_id())
    gestor_reclamo.guardar_reclamo(reclamo_2_2 , cliente_2.get_id())


def departamento_actual(admin_info): 
        # Esta función obtiene el departamento del usuario actual
        # recorriendo la lista de administradores y comparando el id del usuario actual
        for tupla in admin_info:
            if current_user.id == int(tupla[0]):
                departamento = tupla[1]    # Obtener el departamento de la tupla en admin_list      
                return departamento

@login_manager.user_loader  
# Esta función se llama para cargar el usuario actual
# cuando se accede a una ruta protegida por login_required.
def user_loader(user_id):
    # Se busca el usuario en la base de datos por su id
    # y se devuelve el objeto usuario correspondiente.
    return gestor_usuario.consultar_usuario('id',user_id)
    
def is_admin():
    # Esta función verifica si el usuario actual es un administrador
    if current_user.is_authenticated and current_user.id in admin_list:
        return True
    else:
        return False

def admin_only(f):
    """Decorator para restringir el acceso a ciertas vistas solo a administradores."""
    @wraps(f)

    def decorated_function(*args, **kwargs):
        # Verifica si el usuario actual está autenticado y es un administrador
        # Si no lo es, devuelve un error 403 (Forbidden).
        if not current_user.is_authenticated or current_user.id not in admin_list:
            return abort(403) # la función abort() permite devolver errores HTTP de forma sencilla
                              # 403 significa "Forbidden"
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
# Ruta de inicio
def inicio():
    """Renderiza la página de inicio. Si el usuario es un administrador, lo redirige a la vista de administración.
    Si el usuario está autenticado, lo redirige a su vista de usuario."""
    
    if 'username' in session:
        # Si el nombre de usuario está en la sesión, lo asigna a la variable username
        username = session['username']
    else:
        username = 'Invitado'
    
    if is_admin():
        # Si el usuario es un administrador, redirige a la vista de administración
        return redirect(url_for('admin', username=current_user.username))
    elif current_user.is_authenticated:
        # CORRECCIÓN: Ahora redirige a la página de usuario, no de regreso a inicio.
        return redirect(url_for('usuario', username=current_user.username)) 
    
    return render_template('inicio.html', user=username)

@app.route("/login", methods= ["GET", "POST"])
# Ruta de inicio de sesión, utiliza GET y POST
# Esta función maneja el inicio de sesión del usuario.
def login():
    login_form = LoginForm()
    # Acceso a la información ingresada en el formulario
    # cuando el usuario realiza el "submit".
    if login_form.validate_on_submit():
        #hacemos una consulta filtrando por email para
        #saber si hay un usuario registrado con ese email
        user =  gestor_usuario.consultar_usuario('email',login_form.email.data)
        if not user:
            flash("Este email no esta registrado, por favor intenta de nuevo.")
        elif not check_password_hash(user.contrasenia, login_form.password.data):
            flash("Contraseña incorrecta, por favor intenta de nuevo.")
        else:
            login_user(user)
            print(f"Ingresa el usuario: {current_user}")
            session['username'] = user.username
            print(f"nombre de usuario: {session['username']}")

            if is_admin():
                admin_id = current_user.id
                departamento = None
                for admin in admin_info:
                    if admin[0] == admin_id:
                        departamento = admin[1]
                        break
                return redirect(url_for('admin', username=user.username, departamento=departamento))
            else:
                return redirect(url_for('usuario', username=user.username))        
    return render_template('login.html', form=login_form)

@app.route("/register", methods= ["GET", "POST"])
def register():
    register_form = RegisterForm()
    # validate_on_submit verificará si es una solicitud POST y si es válida la información ingresada en el formulario
    if register_form.validate_on_submit():
        # Verifico que no exista usuario con igual email
        if gestor_usuario.consultar_usuario('email',register_form.email.data):
            flash("Ya te has registrado con ese email, ingresa en su lugar!")
            return redirect(url_for('login'))
        # Si el registro es correcto, se crea un nuevo usuario en la db
        encripted_pass = generate_password_hash(
            password= register_form.password.data,
            method= 'pbkdf2:sha256',
            salt_length=8
        )
        gestor_usuario.crear_cliente(register_form.nombre.data, register_form.apellido.data,encripted_pass,
        register_form.username.data, register_form.claustro.data, register_form.email.data)
        return redirect(url_for("login"))
    return render_template('register.html', reg_form = register_form)

# 8) decoramos la vista con login_required para asegurar de que el usuario actual está conectado
# y autenticado antes de llamar a la función

@app.route("/inicio/<username>", methods= ["GET", "POST"])
@login_required
# Ruta para la vista de usuario
# Esta función renderiza la vista de usuario, mostrando su nombre de usuario y una sección específica
def usuario(username):     
    seccion = 'inicio'
    return render_template('usuario.html', user=username, seccion=seccion)                 


@app.route("/inicio/crear_reclamo/<username>", methods= ["GET", "POST"])
@login_required
def crear_reclamo(username):
# Inicializamos las variables que controlan lo que se muestra en la plantilla.
    seccion = 'crear_reclamo'
    reclamos_pendientes = []
    contenido = ""
    mensaje = ""
    mostrar_formulario = True # Por defecto, mostramos el formulario

    # Verificamos si la solicitud es de tipo POST (cuando el usuario envía el formulario)
    if request.method == 'POST':
        # Obtenemos la acción del formulario, que puede ser 'crear_reclamo' o 'confirmar_reclamo'
        action = request.form.get('action')

        # Si la acción es la primera etapa: crear el reclamo
        if action == 'crear_reclamo':
            contenido = request.form.get('detalle-problema', '').strip()
            # Verificamos si el contenido del reclamo no está vacío.
            if not contenido:
                flash("El reclamo no puede estar vacío.")
                # Si está vacío, volvemos a renderizar la página con el error.
            else:
                # Obtenemos los reclamos pendientes para ver si hay duplicados
                reclamo_temporal = gestor_reclamo.crear_reclamo(contenido)
                reclamos_pendientes = gestor_reclamo.reclamos_pendientes(reclamo_temporal.get_nombre_departamento())

                # Si hay reclamos pendientes, pasamos a la etapa de confirmación
                if reclamos_pendientes:
                    mostrar_formulario = False
                else:
                    # Si no hay reclamos pendientes, lo guardamos directamente
                    gestor_reclamo.guardar_reclamo(reclamo_temporal, current_user.id)
                    flash("Reclamo creado con éxito.")
                    return redirect(url_for('mis_reclamos', username=username))

        # Si la acción es la segunda etapa: confirmar el reclamo
        elif action == 'confirmar_reclamo':
            contenido = request.form.get('contenido')
            reclamo = gestor_reclamo.crear_reclamo(contenido)
            gestor_reclamo.guardar_reclamo(reclamo, current_user.id)
            flash("Reclamo creado con éxito.")
            return redirect(url_for('mis_reclamos', username=username))


# Renderizamos la plantilla con las variables actualizadas.
    return render_template('usuario.html',
                            user=username,
                            seccion=seccion,
                            reclamos_pendientes=reclamos_pendientes,
                            contenido=contenido,
                            mostrar_formulario=mostrar_formulario,
                            mensaje=mensaje)

@app.route("/inicio/listar_reclamos/<username>", methods=["GET", "POST"])
# Ruta para listar reclamos
# Esta función renderiza la vista de usuario, mostrando los reclamos pendientes
@login_required

def listar_reclamos(username):
    # Esta función maneja la lógica para listar los reclamos pendientes
    # y filtrar por departamento si se selecciona uno.
    departamentos = ['secretaría técnica', 'maestranza', 'soporte informático']
    departamento_seleccionado = request.form.get('filtro-departamento', 'Todos')
    reclamos_pendientes = []
    seccion = 'listar_reclamos'
    if departamento_seleccionado == 'Todos':
        reclamos_pendientes = gestor_reclamo.reclamos_pendientes()
    else:
        reclamos_pendientes = gestor_reclamo.reclamos_pendientes(departamento_seleccionado)

    return render_template('usuario.html',
                           user=username,
                           reclamos_pendientes=reclamos_pendientes,
                           seccion=seccion,
                           departamentos=departamentos,
                           filtro_departamento=departamento_seleccionado)

@app.route("/inicio/mis_reclamos/<username>", methods= ["GET", "POST"])
@login_required
def mis_reclamos(username):
    reclamos = []
    seccion = 'mis_reclamos'

    if current_user.is_authenticated:
        reclamos = gestor_reclamo.mis_reclamos(current_user.id)
    return render_template('usuario.html',
                        user=username,
                        reclamos=reclamos,
                        seccion=seccion)

@app.route("/inicio/adherirse/<username>", methods= ["GET", "POST"])
@login_required
def adherirse(username):
    seccion = request.form.get('seccion')
    reclamo_id = request.form.get('reclamo_id')
    gestor_reclamo.adherir_usuario(current_user.id, reclamo_id)
    mensaje = "Adherido a reclamo"
    departamento_seleccionado = ''
    reclamos_pendientes = []
    departamentos = ['secretaría técnica', 'maestranza', 'soporte informático']
    
    if seccion == 'listar_reclamos':
        departamento_seleccionado = request.form.get('option')
        if departamento_seleccionado == 'Todos':
            reclamos_pendientes = gestor_reclamo.reclamos_pendientes()
        else:
            reclamos_pendientes = gestor_reclamo.reclamos_pendientes(departamento_seleccionado)

    return render_template('usuario.html',
                           user=username,
                           seccion=seccion,
                           departamentos=departamentos,
                           reclamos_pendientes=reclamos_pendientes,
                           filtro_departamento=departamento_seleccionado,
                           mensaje=mensaje)

@app.route("/admin", methods= ["GET", "POST"])
@admin_only
def admin():   
    departamento = departamento_actual(admin_info)
    
    return render_template('admin.html', departamento=departamento)       

@app.route("/admin/manejar_reclamo", methods= ["GET", "POST"])
@admin_only
def manejar_reclamo():   
    # Esta función maneja la lógica para actualizar el estado de un reclamo
    # y la cantidad de días que lleva en ese estado.
    seccion = 'manejar_reclamo'
    # Verifica si el usuario es un administrador y obtiene su departamento
    departamento = departamento_actual(admin_info)
    if request.method == 'POST':
        reclamo_id = request.form.get('reclamo_id')
        nuevo_estado = request.form.get('nuevo_estado')
        dias_resolucion = request.form.get('dias_resolucion')

        campos_actualizar = {} # Diccionario para almacenar los campos a actualizar
        if nuevo_estado:
                campos_actualizar['estado'] = nuevo_estado 
        
            
        if dias_resolucion:
                campos_actualizar['dias'] = int(dias_resolucion)
                if nuevo_estado == 'en proceso':
                    gestor_reclamo.actualizar_mediana(mediana_proceso, int(dias_resolucion))
                else:
                    gestor_reclamo.actualizar_mediana(mediana_resuelto, int(dias_resolucion))

        gestor_reclamo.actualizar_campos(reclamo_id,campos_actualizar)

    reclamos = gestor_reclamo.todos_los_reclamos(departamento) 
    # Cada reclamo es una tupla con los campos (id, departamento, contenido, estado, dias)
    # Se obtiene la lista de reclamos del departamento del administrador actual
    return render_template('admin.html',
                            reclamos = reclamos,
                            departamento = departamento,
                            seccion= seccion)    
        

@app.route("/admin/derivar_reclamo", methods=["GET", "POST"])
@admin_only
def derivar_reclamo():
    # Esta función maneja la lógica para derivar un reclamo a otro departamento
    # y actualizar el departamento del reclamo.
    departamento = departamento_actual(admin_info)
    campos_actualizar = {}

    if request.method == 'POST':
        # Si se envía el formulario, obtenemos el ID del reclamo y el nuevo departamento
        # y actualizamos el departamento del reclamo.
        reclamo_id = request.form.get('reclamo_id')
        nuevo_departamento = request.form.get('nuevo_departamento')
        
        if nuevo_departamento: 
            campos_actualizar['departamento'] = nuevo_departamento
            gestor_reclamo.actualizar_campos(reclamo_id, campos_actualizar)

    reclamos = gestor_reclamo.todos_los_reclamos() #lista de tuplas

    return render_template('admin.html',
                           reclamos=reclamos,
                           departamento=departamento,
                           seccion='derivar_reclamo')

@app.route("/admin/analitica", methods= ["GET", "POST"])
@admin_only
def analitica():   
    # Esta función maneja la lógica para mostrar la analítica de los reclamos
    # y generar reportes en formato PDF o HTML.
    seccion = 'analitica'
    departamento = departamento_actual(admin_info)
    cant_reclamos_totales = gestor_reclamo.cant_reclamos_tot()
    gestor_reclamo.grafico_circular()
    gestor_reclamo.grafico_palabras()
    mediana_resueltos = gestor_reclamo.mostrar_mediana(mediana_resuelto)
    mediana_en_proceso = gestor_reclamo.mostrar_mediana(mediana_proceso)
    
    if request.method == 'POST':
        # Si se envía el formulario, obtenemos la acción y los reclamos
        # y generamos el reporte correspondiente.
            reclamos = gestor_reclamo.todos_los_reclamos() #lista de tuplas
            if request.form['accion'] == 'descargar_pdf':
                return generar_reporte_pdf(cant_reclamos_totales, mediana_resueltos, mediana_en_proceso,
                                           "static/grafico_circular.png", "static/grafico_palabras.png",
                                           reclamos)
            elif request.form['accion'] == 'descargar_html':
                return generar_reporte_html(cant_reclamos_totales, mediana_resueltos, mediana_en_proceso, 
                                            "static/grafico_circular.png", "static/grafico_palabras.png",
                                            reclamos)
        
    return render_template('admin.html',
                            reclamos_totales = cant_reclamos_totales,
                            mediana_resueltos = mediana_resueltos,
                            mediana_en_proceso = mediana_en_proceso,
                            departamento = departamento,
                            seccion= seccion)      

@app.route("/logout")
def logout():   
    logout_user()      
    session['username'] = 'Invitado' 
    return redirect(url_for('inicio'))
    
def generar_reporte_pdf(reclamos_totales, mediana_resueltos, mediana_en_proceso, grafico_circular, grafico_palabras, reclamos):
    """Genera un reporte en formato PDF con los datos proporcionados y lo devuelve como respuesta para descarga.
    Retorna: (Flask response) Respuesta con el reporte en formato PDF para descargar."""
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Analítica", 0, 1, 'C')
    pdf.cell(200, 10, f"Número de reclamos totales: {reclamos_totales}", 0, 1)
    pdf.cell(200, 10, f"Mediana de reclamos resueltos: {mediana_resueltos}", 0, 1)
    pdf.cell(200, 10, f"Mediana de reclamos en proceso: {mediana_en_proceso}", 0, 1)
    pdf.ln(10)
    pdf.image(grafico_circular, x=10, y=pdf.get_y() + 10, w=100)
    pdf.ln(10)
    pdf.image(grafico_palabras, x=100, y=pdf.get_y() + 10, w=100)
    pdf.ln(80)
    
    pdf.cell(200, 10, "Lista de reclamos", 0, 1)

    # Contenido de la lista de reclamos
    pdf.set_font("Arial", size=12)
    for reclamo in reclamos:
        pdf.ln()
        pdf.cell(0, 10, "ID: {}".format(reclamo[0]), 0, 1)
        pdf.cell(0, 10, "Departamento: {}".format(reclamo[1]), 0, 1)
        pdf.cell(0, 10, "Estado: {}".format(reclamo[3]), 0, 1)
       # Dividir el contenido en líneas más cortas
        contenido = textwrap.wrap(reclamo[2], width=100)  # Longitud máxima de línea: 50 caracteres
        pdf.cell(0, 10, "Contenido:", 0, 1) 
        for linea in contenido:
            pdf.cell(0, 10, linea, 0, 1)

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_analitica.pdf'
    return response


def generar_reporte_html(reclamos_totales, mediana_resueltos, mediana_en_proceso, grafico_circular, grafico_palabras, reclamos):
    """Genera un reporte en formato HTML con los datos proporcionados y lo devuelve como respuesta para descarga.
    Retorna: Respuesta con el reporte en formato HTML para descargar."""
    circular=None 
    palabras = None
    
    with open(grafico_circular,'rb') as archivo:
        circular = archivo.read() 
    with open(grafico_palabras,'rb') as archivo:
        palabras = archivo.read()

    imagen_codificada_circular = base64.b64encode(circular).decode('utf-8')
    imagen_codificada_circular = f'data:image/png;base64,{imagen_codificada_circular}'
    imagen_codificada_palabras = base64.b64encode(palabras).decode('utf-8')
    imagen_codificada_palabras = f'data:image/png;base64,{imagen_codificada_palabras}'

    html_content = render_template('reporte_analitica.html', reclamos_totales=reclamos_totales, mediana_resueltos=mediana_resueltos,
                                    mediana_en_proceso=mediana_en_proceso, reclamos=reclamos,
                                    grafico_palabras=imagen_codificada_palabras, grafico_circular=imagen_codificada_circular)

    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_analitica.html'
    return response



if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')