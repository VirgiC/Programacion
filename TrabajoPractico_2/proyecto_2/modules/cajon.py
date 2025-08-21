from modules.alimento import Alimento

class Cajon:
    def __init__(self): 
        '''El cajon se define con una lista de alimentos y su peso correspondiente
        Posee operaciones para agregar un alimento, conoce los alimentos que tiene y conoce su peso'''
        self.__alimentos_c = []  #inicializacion de atributos
        #__alimentos_c es un atributo muy interno de la clase Cajon. Esto refuerza la idea de que 
        # la lista de alimentos no debe ser modificada directamente desde fuera del cajón, sino a 
        # través de los métodos proporcionados (como agregar_alimento).
        self.__peso_c = 0
    
    def agregar_alimento(self, alimento: Alimento): #Espera recibir un objeto que sea una instancia de la clase Alimento
        self.__alimentos_c.append(alimento) #Añade el alimento recibido al final de la lista interna __alimentos_c
        self.__peso_c += alimento.get_masa()

    def get_peso_c(self): 
        peso_c = self.__peso_c #Recupera el valor del atributo interno __peso_c
        return peso_c
    
    def __len__(self): 
        return len(self.__alimentos_c) #Devuelve el número de alimentos que hay en la lista interna __alimentos_c.
    
    def __iter__(self):
     '''Este metodo permite que el cajon sea iterable'''
     return iter(self.__alimentos_c) #devolver un iterador sobre la lista interna __alimentos_c