from modules.usuario import Usuario
'''La clase SecretarioTecnico hereda de usuario.'''
class SecretarioTecnico(Usuario):
    '''El secretario técnico es un usuario que tiene acceso a los reclamos de todos los departamentos'''
    def __init__(self, nombre, apellido, contrasenia, nombre_usuario, mail):
        super().__init__(nombre, apellido, contrasenia, nombre_usuario, mail)
        
