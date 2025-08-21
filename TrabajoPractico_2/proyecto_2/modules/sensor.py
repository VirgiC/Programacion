import numpy as np
import random
import matplotlib.pyplot as plt

class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su respectivo peso.
    """
    def __init__(self):
        #Inicializa la clase DetectorAlimento con una lista de alimentos y sus pesos.
        
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"] #undefined: si falla la 
        #deteccion
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2) #Creo un array de NumPy con 12 
        #valores de peso, distribuidos uniformemente entre 0.05 y 0.6 kg.
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2) #Calculo las probabilidades 
        #de que se detecte cada peso usando la función __softmax

#Dado que la función Softmax asigna probabilidades más altas a valores de entrada más grandes, 
#el peso 0.6 obtendría la probabilidad más alta, y 0.05 la más baja.

        #El uso de [::-1] invierte el orden de las probabilidades, de modo que el peso más bajo 
        #tenga la probabilidad más baja.
        #Esto significa que los pesos más bajos tienen más probabilidad de ser seleccionados.

    def __softmax(self, x): #Es un método "privado"
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)] #Selecciona un tipo de alimento al azar de la lista self.alimentos.
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]#Selecciona un peso al azar de self.peso_alimentos, pero lo hace ponderando las probabilidades definidas en self.prob_pesos. Esto significa que algunos pesos tienen más chance de ser elegidos que otros.
        return {"alimento": alimento_detectado, "peso": peso_detectado} #Devuelve la información del alimento detectado en un diccionario.
    

if __name__ == "__main__":
    
    random.seed(1)
    sensor = DetectorAlimento()
    lista_pesos = []
    for _ in range(200):
        lista_pesos.append(sensor.detectar_alimento()["peso"])

    plt.hist(lista_pesos, bins=12)
    plt.show()

                

