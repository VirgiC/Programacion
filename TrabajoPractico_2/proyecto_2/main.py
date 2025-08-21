from flask import render_template,request
from modules.cajon import * ##Importa todo (*) lo que está definido en el archivo cajon.py . Esto te permite usar la clase Cajon en este archivo.
from modules.sistema_cinta_transportadora import * 
from modules.config import app

#render_template: Una función de Flask que se usa para "renderizar" (mostrar) archivos HTML. 
#Le pasas un nombre de archivo HTML y los datos que quieres que ese HTML muestre.

#request: Un objeto de Flask que contiene toda la información sobre la petición HTTP 
#que el navegador envió al servidor (si es GET o POST, qué datos se enviaron, etc.).
@app.route("/",methods = ["GET", "POST"]) 
def interfaz(): 
    cinta = Cinta_t()
    cajon = Cajon()
    diccionario = dic()
    '''verificamos si la solicitud es de tipo POST y si contiene el campo cantidad_alimentos antes de intentar acceder'''
    if request.method == "POST" and "cantidad_alimentos" in request.form: #Aquí es donde se manejan las peticiones POST (cuando el usuario ha enviado un formulario).
        cinta.transportar(int(request.form["cantidad_alimentos"]), cajon)
        diccionario = calculos_prom(cajon)
        
    '''Renderiza a la pagina de inicio, interfaz.html'''
  

    return render_template("interfaz.html" , diccionario=diccionario , peso_total = cajon.get_peso_c())
                           


if __name__ == "__main__":
     app.run(debug = True) 
     