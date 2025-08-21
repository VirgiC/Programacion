import unittest
from modules.cajon import Cajon
from modules.manzana import Manzana
from modules.kiwi import Kiwi
from modules.papa import Papa
from modules.fruta import Fruta
from modules.verdura import Verdura
from modules.alimento import Alimento
from modules.zanahoria import Zanahoria
from modules.sistema_cinta_transportadora import *


class Test_Proyecto_2(unittest.TestCase):
        
       def test_transportar(self):
              '''TEST PARA COMPROBAR QUE EL CAJON SE CARGA CON LA CANTIDAD DE ALIMENTOS INDICADA'''
             
              cinta = Cinta_t()
              n_alimentos = 100
              
              for _ in range(100):
                     cajon = Cajon() 
                     cinta.transportar(n_alimentos, cajon)
                     self.assertEqual(n_alimentos, len(cajon))
                     
 
       def test_aws(self):
              '''TEST PARA CHEQUEAR EL CALCULO DE LAS ACTIVIDADES ACUOSAS'''
              cajon = Cajon()
              calculadora = Calculadora()
              cajon.agregar_alimento(Manzana(0.10))
              cajon.agregar_alimento(Kiwi(0.15))
              cajon.agregar_alimento(Papa(0.10))
              cajon.agregar_alimento(Zanahoria(0.15))
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Manzana),5),0.67154) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Kiwi),5),0.83909) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Fruta),5),0.75531) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Verdura),5),0.72392) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Papa),5),0.70204) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Zanahoria),5),0.74580) 
              self.assertEqual(round(calculadora.calcular_promedio_aw(cajon,Alimento),5),0.73962) 
        
       def test_de_tipos(self):
              '''TEST PARA CHEQUEAR LOS TIPOS DE OBJETOS EN CAJON'''
              cajon = Cajon() 
              cajon.agregar_alimento(Manzana(0.10))
              cajon.agregar_alimento(Kiwi(0.15))
              cajon.agregar_alimento(Papa(0.10))
              cajon.agregar_alimento(Zanahoria(0.15))
              for alimento in cajon:
                     self.assertIsInstance(alimento, Alimento)
              
        
       def test_peso_cajon(self):
              '''TEST PARA CHEQUEAR EL PESO DEL CAJON'''
              cajon = Cajon() 
              manzana = Manzana(0.10)
              kiwi = Kiwi(0.10)
              papa = Papa(0.15)
              zanahoria = Zanahoria(0.15)
              cajon.agregar_alimento(manzana)
              cajon.agregar_alimento(kiwi)
              cajon.agregar_alimento(papa)
              cajon.agregar_alimento(zanahoria)
              peso_prueba = manzana.get_masa() + kiwi.get_masa() + papa.get_masa() + zanahoria.get_masa()
              self.assertEqual(cajon.get_peso_c(),peso_prueba)
              
 

if __name__ == "__main__":
       unittest.main()
