import unittest
from modules.clasificador import Clasificador

class TestClasificador(unittest.TestCase):


 def test_clasificar_reclamo(self):
  """Testea el método clasificar_reclamo del clasificador."""
  clasificador=Clasificador()
  eleccion =  clasificador.clasificar_reclamo('La computadora de la sala de computacion no esta funcionando')
  self.assertEqual(eleccion,'soporte informático')
  eleccion =  clasificador.clasificar_reclamo('El sistema de climatización en el aula B-2 está fallando.')
  self.assertEqual(eleccion,'secretaría técnica')
  eleccion =  clasificador.clasificar_reclamo('El baño del modulo 1 se encuentra fuera de servicio')
  self.assertEqual(eleccion,'maestranza')

if __name__ == '__main__':
    unittest.main()

  
