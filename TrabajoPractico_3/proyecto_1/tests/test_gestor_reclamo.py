import unittest
import os
from modules.gestor_reclamos import GestorReclamo
from modules.gestor_db import GestorDB
from modules.config import app,db

with app.app_context():
    gestor_db = GestorDB(db)

class TestGestorReclamo(unittest.TestCase):
    '''Test para comprobar que un reclamo se creó correctamente'''
    def test_crear_reclamo(self):
        
        gestor_reclamo = GestorReclamo(gestor_db)
        # Creamos un reclamo con un contenido de prueba
        # y verificamos que se haya creado correctamente.
        reclamo = gestor_reclamo.crear_reclamo("Este es un reclamo de prueba.")
        
        # Verificamos que el reclamo no sea None y que tenga un ID
        self.assertEqual(reclamo.get_contenido(), "Este es un reclamo de prueba.")
        self.assertIsNotNone(reclamo.get_nombre_departamento())

    def test_grafico_circular(self):
        gestor_reclamo = GestorReclamo(gestor_db)

        with app.app_context():
            # Llamamos al método grafico_circular
            gestor_reclamo.grafico_circular()

        # Verificamos que el archivo de imagen se haya creado correctamente
        ruta_guardado_circular = os.path.join(os.path.dirname(__file__), '..', 'static', 'grafico_circular.png')
        self.assertTrue(os.path.exists(ruta_guardado_circular), "El gráfico circular no se generó correctamente.")


        # Limpiar (eliminar) el archivo generado después de la prueba
        if os.path.exists(ruta_guardado_circular):
            os.remove(ruta_guardado_circular)

    def test_grafico_palabras(self):
        gestor_reclamo = GestorReclamo(gestor_db)

        with app.app_context():
            # Llamamos al método grafico_palabras
            gestor_reclamo.grafico_palabras()

        # Verificamos que el archivo de imagen se haya creado correctamente
        ruta_guardado_palabras = os.path.join(os.path.dirname(__file__), '..', 'static', 'grafico_palabras.png')
        self.assertTrue(os.path.exists(ruta_guardado_palabras), "La nube de palabras no se generó correctamente.")


        # Limpiar (eliminar) el archivo generado después de la prueba
        if os.path.exists(ruta_guardado_palabras):
            os.remove(ruta_guardado_palabras)
    

if __name__ == '__main__':
    unittest.main()


