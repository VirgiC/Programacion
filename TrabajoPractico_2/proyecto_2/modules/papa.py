from modules.verdura import Verdura
from numpy import arctan

class Papa(Verdura):
     '''clase papa que hereda todo de verdura'''
     def __init__(self,masa):
      super().__init__(masa)
      self._masa
      self._aw
      self.calcular_aw()

     
     def calcular_aw(self):
          self._aw = 0.66*(arctan(18*self._masa)) #La funcion arctan toma el angulo en radianes...