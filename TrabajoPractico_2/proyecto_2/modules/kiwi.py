from modules.fruta import Fruta
import math

class Kiwi(Fruta):
    '''Clase kiwi que hereda todo de la clase fruta'''
    def __init__(self, masa):
          super().__init__(masa)
          self._masa
          self._aw
          self.calcular_aw() 

          

    def calcular_aw(self):
          self._aw = 0.96 * ((1 - math.exp(-18 * self._masa)) / (1 + math.exp(-18 * self._masa)))
          
    

    