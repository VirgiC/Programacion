from modules.config import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
'''SQLAlchemy nos permite trabajar con bases de datos relacionales '''

'''Flask_Login nos brinda una clase UserMixin de la cual heredamos metodos y atributos necesarios para facilitar el manejo del
login de los usuarios'''

'''db.Model es una clase base de SQLAlchemy que se utiliza para definir modelos de datos en una aplicación Flask. 
Esta clase proporciona una interfaz para interactuar con la base de datos utilizando
objetos Python que representan las tablas y columnas de la base de datos. '''

'''__tablename__ corresponde al nombre de la tabla SQL dentro de la base de datos'''

'''primary_key es un campo o conjunto de campos que identifica de manera única cada
    registro en una tabla. Suele ser un campo numérico autoincremental. 
   
    Un campo numérico autoincremental es una columna en una tabla de base de datos que automáticamente 
    genera un valor numérico único e incremental cada vez que se inserta una nueva fila en la tabla.
    Este tipo de campo es comúnmente utilizado para las claves primarias de las tablas, 
    asegurando que cada fila tenga un identificador único sin necesidad de que el usuario proporcione manualmente el valor.
    
    primary_key no permite valores duplicados y que se utiliza como índice para acceder a los registros 
    de la tabla de forma rápida y eficiente'''

'''Una clave foránea (Foreign Key) es un campo en una tabla que se utiliza para establecer y reforzar un vínculo entre los datos en dos tablas. Es un mecanismo para asegurar la integridad referencial de los datos.
 Una clave foránea en una tabla es un campo que apunta a la clave primaria en otra tabla.'''


#_____________________________________________________________________________________________________________#

'''Tabla de asociacion: Establece una relación muchos a muchos entre usuarios y reclamos. 
Una relación muchos a muchos ocurre cuando los registros de una tabla pueden estar relacionados con 
múltiples registros de otra tabla, y viceversa.

Cada usuario puede seguir múltiples reclamos y cada reclamo puede ser seguido por múltiples usuarios.'''
'''Define una columna reclamo_id que es una clave foránea referenciando la columna id de la tabla reclamos.'''
'''Define una columna user_id que es una clave foránea referenciando la columna id de la tabla usuario.'''

asociacion_usuarios_reclamos = db.Table('usuario_reclamo', 
    Column('user_id', Integer, ForeignKey('usuario.id')),
    Column('reclamo_id', Integer, ForeignKey('reclamos.id')))
#Esta tabla no almacena información de reclamos ni de usuarios. Su único propósito es conectar los 
#registros de las otras dos tablas. Cada fila en asociacion_usuarios_reclamos representa una conexión.

'''Define la estructura de la tabla usuario con varios campos y establece una relación muchos a muchos con TablaReclamos.'''
class TablaUsuario(UserMixin, db.Model):
    #la clase TablaUsuario hereda de db.Model y le dices a SQLAlchemy que esta clase representa una 
    #tabla en la base de datos llamada tabla_usuarios.
    __tablename__ = 'usuario'
    '''Define como clave primaria el ID del usuario'''
    id = Column(Integer, primary_key=True)
    '''Column(..., nullable=False, unique=True): Define columnas que no pueden ser nulas y deben ser únicas.'''
    nombre = Column(String(1000), nullable=False, unique=True)
    apellido = Column(String(1000), nullable=False)
    email = Column(String(1000), nullable=False, unique=True)
    contrasenia = Column(String(1000), nullable=False)
    username = Column(String(1000), nullable=False, unique=True)
    claustro = Column(String(1000), nullable=False)
    
    '''Establece una relación muchos a muchos con TablaReclamos''' 

    reclamos_seguidos = relationship('TablaReclamos', secondary = asociacion_usuarios_reclamos, backref = 'usuarios_seguidores')
    
    ''' * Especifica la clase relacionada, en este caso, TablaReclamos,
        * secondary = asociacion_usuarios_reclamos: Especifica la tabla de asociación que se utiliza para la relación muchos a muchos. 
       asociacion_usuarios_reclamos es una tabla intermedia que conecta Usuario con Reclamo.
        * backref = El parámetro backref en SQLAlchemy se utiliza para crear una relación inversa entre dos tablas. 
        Cuando defines una relación usando backref, SQLAlchemy automáticamente agrega una propiedad en 
        la clase relacionada que permite acceder a la relación inversa (de uno a muchos) sin necesidad de definir explícitamente otra relationship '''

'''Define la estructura de la tabla reclamos y establece una relación uno a muchos con TablaUsuario.'''
class TablaReclamos(db.Model):
    __tablename__ = 'reclamos'
    '''Define como clave primaria el ID del reclamo'''
    id = Column(Integer, primary_key=True)
    departamento = Column(String(1000), nullable=False)
    contenido = Column(String(1000), nullable=False)
    estado = Column(String(1000), nullable=False)
    ''' Define id_usuario como una clave foránea que referencia la columna id de la tabla usuario.'''
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    fecha = Column(String(1000), nullable=False)
    dias = Column(Integer, nullable=True)
    

    
    
    
   
    

    


