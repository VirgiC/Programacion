from modules.verdura import Verdura
import math

class Zanahoria(Verdura):
     '''clase zanahoria que hereda todo de verdura'''
     def __init__(self,masa):
      super().__init__(masa)
      self._masa
      self._aw
      self.calcular_aw() 

     
     def calcular_aw(self):
          self._aw = 0.96 * (1 - math.exp(-10 * self._masa))