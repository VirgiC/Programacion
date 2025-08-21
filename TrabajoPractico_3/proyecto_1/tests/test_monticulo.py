import unittest
from modules.monticulo import Monticulo

class TestMonticulo(unittest.TestCase):

    def test_monticulo(self):
        mont = Monticulo()

        ''' Insertar elementos en el montículo de máximo'''
        mont.insertar(10)
        mont.insertar(20)
        mont.insertar(5)

        ''' Verificar el tamaño del montículo'''
        self.assertEqual(mont.tamanio(), 3)

        ''' Eliminar la raíz del montículo'''
        self.assertEqual(mont.eliminar_raiz(), 20)

        ''' Eliminar la raíz del montículo'''
        self.assertEqual(mont.eliminar_raiz(), 10)

        ''' Verificar encontrar_hijo en montículo '''
        mont.insertar(30)
        mont.insertar(40)
        '''encontrar_hijo devuelve el indice del nodo hijo'''
        self.assertEqual(mont.encontrar_hijo(1), 3)

if __name__ == '__main__':
    unittest.main()