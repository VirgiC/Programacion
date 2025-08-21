from modules.monticulo import Monticulo

class MonticuloMediana():
   
    def __init__(self):
        self.__monticulo_min = Monticulo(True)
        self.__monticulo_max = Monticulo() 
        self.__mediana = 0
      
    def calcular_mediana(self, lista):
        if lista:
            for elemento in lista:
                if self.__mediana < elemento:
                    '''se lo compara con la mediana, si es mayor a esta, lo insertamos en el montículo de mínimos'''
                    self.__monticulo_min.insertar(elemento)
                else: #que pasaria si el valor fuera igual a la mediana?
                    '''Si el número es menor a la mediana, lo insertamos en el montículo de máximos. '''
                    self.__monticulo_max.insertar(elemento)
               
                
                '''Verificar que la diferencia entre el número de elementos de los 2 montículos no sea mayor a 1.'''
                if abs(self.__monticulo_max.tamanio() - self.__monticulo_min.tamanio()) > 1:
                    ''' Si la diferencia es mayor a 1, tomamos la raíz del montículo de mayor tamaño y lo insertamos en el otro montículo.'''
                    '''Si el de mayor tamaño es el monticulo de maximo:'''
                    if self.__monticulo_max.tamanio() > self.__monticulo_min.tamanio():
                        raiz = self.__monticulo_max.eliminar_raiz()
                        self.__monticulo_min.insertar(raiz)
                    else: 
                        '''Sino, el de mayor tamaño es el monticulo de minimo:'''
                        raiz = self.__monticulo_min.eliminar_raiz()
                        self.__monticulo_max.insertar(raiz)
               
                ''' Calculamos la nueva mediana. Si ambos montículos tienen el mismo número de elementos,la mediana es el promedio de las raíces de los 2 montículos'''
                if self.__monticulo_max.tamanio() == self.__monticulo_min.tamanio():
                    self.__mediana =float( (self.__monticulo_max.get_raiz() +  self.__monticulo_min.get_raiz())/2 )
                
                else:
                    '''Si los montículos tienen distinto número de elementos...'''
                    '''La mediana será el valor de la raíz del montículo de mayor tamaño.'''
                    if self.__monticulo_max.tamanio() > self.__monticulo_min.tamanio():
                        self.__mediana = self.__monticulo_max.get_raiz() 
                    else: 
                        self.__mediana = self.__monticulo_min.get_raiz()

    
    def actualizar_mediana(self, elemento):
        '''Esta funcion sigue la misma logica que calcular_mediana, pero con el elemento que toma como parametro'''
        '''Surge la necesidad de este metodo porque la lista puede ir cambiando en el tiempo cuando llegan nuevos valores.'''
        if self.__mediana < elemento:
            self.__monticulo_min.insertar(elemento)
        else: 
            self.__monticulo_max.insertar(elemento)

        if abs(self.__monticulo_max.tamanio() - self.__monticulo_min.tamanio()) > 1:
            if self.__monticulo_max.tamanio() > self.__monticulo_min.tamanio():
                raiz = self.__monticulo_max.eliminar_raiz()
                self.__monticulo_min.insertar(raiz)
            else: 
                raiz = self.__monticulo_min.eliminar_raiz()
                self.__monticulo_max.insertar(raiz)
        
        if self.__monticulo_max.tamanio() == self.__monticulo_min.tamanio():
            self.__mediana = float((self.__monticulo_max.get_raiz() +  self.__monticulo_min.get_raiz())/2 )
        else:
            if self.__monticulo_max.tamanio() > self.__monticulo_min.tamanio():
                self.__mediana = self.__monticulo_max.get_raiz() 
            else: 
                self.__mediana = self.__monticulo_min.get_raiz()


    def get_mediana(self):
        mediana=self.__mediana
        return  mediana

