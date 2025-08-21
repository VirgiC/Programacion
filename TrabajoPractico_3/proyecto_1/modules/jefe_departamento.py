from modules.usuario import Usuario
'''Definimos la clase JefeDeDepartamento, que hereda directamente desde usuario'''
class JefeDeDepartamento(Usuario):
    '''El jefe de departamento es un usuario que tiene acceso a los reclamos de su departamento'''
    def __init__(self, nombre, apellido, contrasenia, nombre_usuario, mail):
        super().__init__(nombre, apellido, contrasenia, nombre_usuario, mail)
        