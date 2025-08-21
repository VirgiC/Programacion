from modules.funciones import *
from server import *
if __name__ == "__main__":  
    generar_graficas_eje_coordenado()
    generar_grafico_circular()

    archivo_docs = "datos_partidas.txt"
    lista_fechas = listar_fechas(archivo_docs) 
    lista_aciertos_acumulados = acumular_aciertos(archivo_docs, lista_fechas)
    lista_desaciertos_acumulados = acumular_desaciertos(archivo_docs,lista_fechas,lista_aciertos_acumulados)
    print(lista_fechas)
    print("\n\n")
    print("aciertos totales: " ) 
    print(lista_aciertos_acumulados)
    print("\n\n")
    print("desaciertos totales: ")
    print(lista_desaciertos_acumulados) 
    generar_archivo_pdf()

    
    