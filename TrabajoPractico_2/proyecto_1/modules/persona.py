from abc import ABC
class Persona(ABC): 
   '''Definimos los parametros de una persona y los metodos para obtener esos parametros.'''
   '''Clase Persona es una clase abstracta (no es posible instanciarla)'''
   def __init__(self, nombre, edad): 
         self._nombre = nombre
         self._edad = edad 

        
   def set_nombre(self, nombre):
         self._nombre = nombre
         
   def set_edad(self, edad):
           if edad >= 0:
            self._edad = edad
           else:
            raise Exception("La edad no puede ser negativa")        
        
   def get_edad(self):
           edad = self._edad
           return edad
           
   def get_nombre(self):
           nombre = self._nombre
           return nombre