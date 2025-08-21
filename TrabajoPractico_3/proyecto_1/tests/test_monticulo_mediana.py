import unittest 
from modules.monticulo_mediana import MonticuloMediana

class TestMonticuloMediana(unittest.TestCase):

    def test_calculo_mediana(self):
        '''TEST PARA COMPROBAR QUE EL CALCULO DE MEDIANA SE REALICE CORRECTAMENTE'''
        lista_par = [5,7,1,6,3,8,9,15]
        lista_impar = [5,7,1,6,3,8,9] 
        mont = MonticuloMediana()
        mont2 = MonticuloMediana()
        
        mont.calcular_mediana(lista_impar)
        self.assertEqual(mont.get_mediana(),6)
        
        mont2.calcular_mediana(lista_par)
        self.assertEqual(mont2.get_mediana(),6.5)

        mont2.actualizar_mediana(9) 

        self.assertEqual(mont2.get_mediana(),7)
  
if __name__ == '__main__':
    unittest.main()

