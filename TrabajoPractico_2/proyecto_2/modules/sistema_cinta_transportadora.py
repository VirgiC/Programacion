from modules.cajon import Cajon
from modules.manzana import Manzana
from modules.fruta import Fruta 
from modules.verdura import Verdura
from modules.kiwi import Kiwi
from modules.zanahoria import Zanahoria
from modules.papa import Papa
from modules.sensor import DetectorAlimento
from modules.alimento import Alimento

def dic():
     '''Simplemente crea y devuelve un diccionario predefinido con claves para los 
     diferentes promedios de actividad acuosa, todos inicializados a 0.0. 
     Esto sirve como una estructura base para los resultados.'''

     diccionario = {'promedio_aw_general':0.0, 'promedio_aw_verdura':0.0,'promedio_aw_fruta':0.0,'promedio_aw_manzana':0.0
                       ,'promedio_aw_kiwi':0.0,'promedio_aw_zanahoria':0.0,'promedio_aw_papa':0.0}
     return diccionario

def calculos_prom(cajon):
    calculadora = Calculadora()
    diccionario = dic()
    diccionario['promedio_aw_verdura'] = calculadora.calcular_promedio_aw(cajon, Verdura)
    diccionario ['promedio_aw_fruta'] = calculadora.calcular_promedio_aw(cajon, Fruta)
    diccionario['promedio_aw_kiwi'] = calculadora.calcular_promedio_aw(cajon, Kiwi)
    diccionario['promedio_aw_manzana'] = calculadora.calcular_promedio_aw(cajon, Manzana)
    diccionario['promedio_aw_papa'] = calculadora.calcular_promedio_aw(cajon, Papa)
    diccionario['promedio_aw_zanahoria'] = calculadora.calcular_promedio_aw(cajon, Zanahoria)
    diccionario['promedio_aw_general'] = calculadora.calcular_promedio_aw(cajon, Alimento) #calcula el promedio general usando la clase Alimento como filtro.
    return diccionario


class Calculadora:
    def __init__(self):
     '''La clase Calculadora modela una calculadora que es capaz de calcular el promedio de actividades acuosas
     de alimentos que estan dentro de un cajon'''
     pass    

    def calcular_promedio_aw(self, cajon:Cajon, p_clase ): #p_clase: Este parámetro es el tipo de clase de alimento por el cual se quiere filtrar (ej., Verdura, Fruta, Kiwi, Alimento mismo).
        '''Calcular_promedio_aw recibe el cajon y la clase de alimento correspondiente.
        Establece el promedio de la actividad acuosa dependiendo del tipo de alimento al recorrer cajon'''
        cont = 0
        promedio = 0.0

        for alimento in cajon:
            if isinstance(alimento, p_clase): #isinstance() verifica si el alimento actual en el bucle es una instancia de la p_clase especificada 
                promedio += alimento.get_aw() #Suma la actividad acuosa del alimento si coincide con la clase.
                cont += 1 # Lleva la cuenta de cuántos alimentos de esa clase se encontraron.

        if cont > 0:
            promedio = promedio/cont
        if cont == 0:
            promedio = 0.0
        #aseguran que no se intente dividir por cero si no se encontraron alimentos del tipo buscado, devolviendo 0.0 en ese caso
        return promedio
    

class Cinta_t:
    def __init__(self):
        '''Cinta_t representa una cinta transportadora que incluye un sensor, esta cinta transporta alimentos para cargarlos en un cajon'''
        self.__sensor = DetectorAlimento() #Crea una instancia del DetectorAlimento
        #Esto significa que la cinta tiene su propio sensor.
        
    def transportar(self, n_alimentos : int, cajon:Cajon):
        '''Transportar hace uso de sensor, sensor los va detectando y
         al transportar los alimentos se agregan al cajon'''
        
        i = 0
        while i < n_alimentos: # Se asegura de que se procesen n_alimentos que sean válidos (no undefined).
            deteccion = self.__sensor.detectar_alimento() #Detecta un alimento y su peso usando el sensor.
            if deteccion['alimento']=='undefined':
                continue

            #Para crear instancias de alimento: Basado en el alimento detectado por el sensor
            elif deteccion['alimento']=='kiwi':
                alimento = Kiwi(float(deteccion['peso']))
            elif deteccion['alimento']=='manzana':
                alimento = Manzana(float(deteccion['peso']))
            elif deteccion['alimento']=='papa':
                alimento = Papa(float(deteccion['peso']))
            else:
                alimento = Zanahoria(float(deteccion['peso']))

            cajon.agregar_alimento(alimento) #Una vez que se crea el objeto alimento, se llama al método agregar_alimento del cajon para añadirlo.
            i += 1
    
    
      
        

    
         
    