class Monticulo():
    '''
    Clase que implementa un montículo (heap) para almacenar elementos de manera ordenada. 
    Permite insertar elementos, eliminar la raíz y mantener la propiedad del montículo.
    Puede ser un montículo de máximo o de mínimo, dependiendo del parámetro opcional 'cond'.
    '''

    def __init__(self, cond = None):
       ''' Inicializa un montículo  vacío. '''
       '''Condicional que permite conocer si el monticulo es de maximo o de minimo, recibe la 
       cond como parametro opcional'''
       '''por defecto es de maximo'''
       self.__es_min = False 
       if cond:
            self.__es_min = True
       '''La listaMonticulo se inicializa con un valor en la primera posicion'''
       self.__lista_monticulo = [0]  
  
   

    def insertar(self, k):
        '''
        Inserta un nuevo elemento en el montículo.

        Parámetros:
        - k: Elemento a insertar en el montículo.
        '''
        self.__lista_monticulo.append(k)
        self.infiltrar_hacia_arriba(len(self.__lista_monticulo) - 1)
    
    def tamanio(self):
        '''
        Retorna:
        - Tamaño del montículo.
        '''
        return len(self.__lista_monticulo) - 1
    
    def eliminar_raiz(self):
     if len(self.__lista_monticulo) > 1:
                '''La raiz está en la posición 1'''
                raiz = self.__lista_monticulo[1]  # 
                '''Elimina el último elemento de la lista'''
                ultimo = self.__lista_monticulo.pop()  
                if len(self.__lista_monticulo) > 1:
                        '''Mueve el último elemento a la cima del montículo'''
                        self.__lista_monticulo[1] = ultimo 
                        '''Llama a la función infiltrar_hacia_abajo para restaurar la propiedad del montículo''' 
                        self.infiltrar_hacia_abajo(1)  
     return raiz
    
    def get_raiz(self):
         raiz = self.__lista_monticulo[1]
         return raiz

    def encontrar_hijo(self, i):
    
        '''
        Encuentra el índice del hijo en un nodo dado.

        Parámetros:
        - i: Índice del nodo padre.

        Retorna:
        - Índice del hijo.
        '''
        if (i * 2 + 1) > self.tamanio():
            return i * 2
        else:
            hijo_izquierdo = i * 2
            hijo_derecho = i * 2 + 1

            if self.__es_min == False: 
                # Comparar las distancias en lugar de los vértices directamente
                if self.__lista_monticulo[hijo_izquierdo] > self.__lista_monticulo[hijo_derecho]:
                    return hijo_izquierdo
                else:
                    return hijo_derecho
            
            else: 
                    if self.__lista_monticulo[hijo_izquierdo] < self.__lista_monticulo[hijo_derecho]:
                        return hijo_izquierdo
                    else:
                        return hijo_derecho

    def infiltrar_hacia_arriba(self, i):
        '''
        Realiza la operación "infiltrar_hacia_arriba" para mantener la propiedad del montículo después de una inserción.

        Parámetros:
        - i: Índice del elemento que se ha insertado.
        '''
        if self.__es_min == False: 
            while i // 2 > 0:
                if self.__lista_monticulo[i] > self.__lista_monticulo[i // 2]:
                    self.__lista_monticulo[i], self.__lista_monticulo[i // 2] = self.__lista_monticulo[i // 2], self.__lista_monticulo[i]
                i = i // 2
        else: 
            while i // 2 > 0:
                if self.__lista_monticulo[i] < self.__lista_monticulo[i // 2]:
                    self.__lista_monticulo[i], self.__lista_monticulo[i // 2] = self.__lista_monticulo[i // 2], self.__lista_monticulo[i]
                i = i // 2

    def infiltrar_hacia_abajo(self, i):
        '''
        Realiza la operación "bajar" para mantener la propiedad del montículo después de una eliminación.

        Parámetros:
        - i: Índice del elemento que se ha eliminado.
        '''
        if self.__es_min == False:
            while (i * 2) <= self.tamanio():
                hijoMaximo = self.encontrar_hijo(i)
                if self.__lista_monticulo[i] < self.__lista_monticulo[hijoMaximo]:
                    self.__lista_monticulo[i], self.__lista_monticulo[hijoMaximo] = self.__lista_monticulo[hijoMaximo], self.__lista_monticulo[i]
                i = hijoMaximo

        else:
            while (i * 2) <= self.tamanio():
                    hijoMinimo = self.encontrar_hijo(i)
                    if self.__lista_monticulo[i] > self.__lista_monticulo[hijoMinimo]:
                        self.__lista_monticulo[i], self.__lista_monticulo[hijoMinimo] = self.__lista_monticulo[hijoMinimo], self.__lista_monticulo[i]
                    i = hijoMinimo
        

         