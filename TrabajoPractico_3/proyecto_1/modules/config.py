from flask import Flask
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from datetime import timedelta


'''Se crea una instancia de la aplicación Flask con el nombre "server".'''
app = Flask("server")


'''La clave secreta se utiliza para proteger sesiones y datos de CSRF (Cross-Site Request Forgery). 
Es importante mantener esta clave segura y no compartirla públicamente.'''

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


'''Estas líneas configuran la conexión a la base de datos SQLite llamada users.db y
 deshabilitan el seguimiento de modificaciones para evitar sobrecarga innecesaria.'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
'''app.app_context() crea un contexto de aplicación Flask. 
    Esto es necesario porque algunas operaciones, como la creación de tablas en SQLAlchemy, 
    requieren acceder a la configuración de la aplicación Flask y a la sesión de base de datos 
    que están asociadas a esa aplicación.'''

db = SQLAlchemy(app)

'''Flask-WTF'''
app.config["WTF_CSRF_ENABLED"] = False

''' Por defecto, Flask-WTF habilita la protección CSRF de forma automática. 
 Cuando esta protección está habilitada, cada formulario generado con Flask-WTF 
 incluirá un token CSRF único que se espera que el navegador incluya en cada solicitud POST. 
Si el token CSRF no coincide con el servidor, la solicitud POST se considera potencialmente
 maliciosa y se rechaza.'''


'''Configura Flask-Session para almacenar las sesiones en el sistema de archivos 
(filesystem) con una vida útil de sesión no permanente de 5 minutos. 
Session(app) inicializa la extensión Flask-Session en la aplicación.'''
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = timedelta(minutes=50)
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config.from_object(__name__)
Session(app)

''' Bootstrap: Inicializa la extensión Flask-Bootstrap en la aplicación, 
que proporciona estilos y componentes HTML/CSS de Bootstrap.'''
Bootstrap(app)

'''Configura Flask-Login para manejar la autenticación de usuarios. 
 * login_manager.init_app(app) :inicializa la extensión en la aplicación Flask.
 * login_manager.login_view = 'login' especifica la vista de inicio de sesión en caso de que un usuario no autenticado intente acceder a una página protegida.'''
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'