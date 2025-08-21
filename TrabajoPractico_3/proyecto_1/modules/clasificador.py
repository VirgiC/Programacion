import pickle # Importa la librería pickle para manejar archivos de objetos serializados
import os # Importa la librería os para manejar rutas de archivos

class Clasificador:
    '''Clase que utiliza el clasificador de reclamos para clasificar un reclamo dado.'''
    def __init__(self): 
        pass

    def clasificar_reclamo(self, contenido:str):
        ''' Obtener la ruta absoluta del directorio actual '''
        ruta = os.path.dirname(os.path.abspath(__file__))
        ''' Unir la ruta absoluta con la ruta al archivo '''
        clf_path = os.path.join(ruta, '..', 'data', 'claims_clf.pkl')
        ''' Abrir el archivo con el clasificador y guardarlo en la variable clf '''
        with open(clf_path, 'rb') as archivo:
            clf = pickle.load(archivo)
        return clf.clasificar([contenido]) #Utiliza el método clasificar del clasificador
        # Devuelve la clasificación del reclamo


