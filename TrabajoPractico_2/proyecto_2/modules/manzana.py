from modules.fruta import Fruta

class Manzana(Fruta):
     '''Clase manzana que hereda todo de fruta'''
     def __init__(self, masa):
          super().__init__(masa)
          self._masa 
          self._aw 
          self.calcular_aw()
 
          

     def calcular_aw(self):
         self._aw = 0.97 * ((15 * self._masa)**2 / (1 + (15 * self._masa)**2))

          
     