from modules.usuario import Usuario
'''Definimos la clase Cliente que hereda de Usuario'''
class Cliente(Usuario):
    '''El cliente es un usuario que tiene acceso a los reclamos de su claustro'''
    # El claustro puede ser "alumno", "docente" o "no docente"
    def __init__(self, nombre, apellido, contrasenia, nombre_usuario, claustro, mail):
        super().__init__(nombre, apellido,contrasenia, nombre_usuario, mail)
        self.__claustro = claustro 
       
    
    def get_claustro(self):
        '''Devuelve el claustro del cliente'''
        return self.__claustro
