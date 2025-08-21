from abc import ABC, abstractmethod

class Alimento(ABC): 
  # clase abstacta que no puede ser instanciada directamente, su proposito es ser heredada por otras clases
  def __init__(self, masa:float): # Es el constructor de la clase, se llama cada vez que se crea una instancia de una subclase de Alimento
    self._masa = masa # atributo "protegido" o "interno" (_)
    self._aw=None  # Este valor se calculará más tarde por las subclases.            

  def get_masa(self): #Permite a otras partes del programa obtener el valor de la masa de un alimento sin acceder directamente al atributo interno _masa
    masa = self._masa
    return masa

  def get_aw(self): 
    aw = self._aw
    return aw

  @abstractmethod
  def calcular_aw(self): 
    '''Metodo Virtual'''
    pass
     
#cualquier subclase que herede de Alimento (como Manzana, Kiwi, Papa, Zanahoria) DEBE 
# implementar su propia versión de calcular_aw().
# pass: Se usa aquí porque este método en la clase base no tiene una implementación 
# concreta; solo declara que debe existir en las subclases.
