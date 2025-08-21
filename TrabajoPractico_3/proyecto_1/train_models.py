# train_models.py (Versión que ya te di, que usa gestor_db.todos_los_reclamos())
import pandas as pd
import pickle
import os

# Importar las clases necesarias de tu proyecto
from modules.classifier import ClaimsClassifier
from modules.config import app, db # Importamos app y db desde config.py
from modules.gestor_db import GestorDB
from modules.reclamo import Reclamo # Para trabajar con objetos Reclamo si es necesario

print("Iniciando el proceso de reentrenamiento del modelo...")

# --- 1. Extraer los datos de entrenamiento de la base de datos ---
# Necesitamos estar dentro del contexto de la aplicación Flask para acceder a 'db'
with app.app_context():
    gestor_db = GestorDB(db)

    # Ahora sabemos que gestor_db.todos_los_reclamos() es el método correcto.
    # Devuelve una lista de tuplas: (reclamo_obj, id_usuario_creador, adherentes, dias)
    all_claims_data_from_db = gestor_db.todos_los_reclamos()
    
    X_train = []
    y_train = []
    
    for reclamo_obj, _, _, _ in all_claims_data_from_db: # Desempacamos para obtener solo el objeto reclamo
        if reclamo_obj.get_contenido() and reclamo_obj.get_nombre_departamento():
            X_train.append(reclamo_obj.get_contenido())
            y_train.append(reclamo_obj.get_nombre_departamento())

    if not X_train:
        print("¡ADVERTENCIA! No se encontraron reclamos en la base de datos con contenido y departamento para entrenar.")
        print("Usando datos de ejemplo para demostración. ¡Esto no entrenará un modelo útil para tu aplicación real!")
        X_train = ["problema con la luz", "fuga de agua en el baño", "el ascensor no funciona", "necesito asistencia con el cable", "problema con el drenaje"]
        y_train = ["electricidad", "plomeria", "mantenimiento", "tecnologia", "plomeria"]
    else:
        print(f"Datos de entrenamiento extraídos de la base de datos. {len(X_train)} ejemplos.")

print("\nIniciando el reentrenamiento de ClaimsClassifier...")

# --- 2. Instanciar y entrenar el ClaimsClassifier ---
classifier = ClaimsClassifier()
classifier.fit(X_train, y_train)

print("ClaimsClassifier entrenado exitosamente.")

# --- 3. Guardar el modelo entrenado ---
# Obtener la ruta absoluta para guardar el modelo
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'claims_clf.pkl')
#"serializa" (guarda) el pipeline completo ya entrenado.

with open(output_path, 'wb') as file:
    pickle.dump(classifier, file)

print(f"Modelo guardado en: {output_path}")
print("\nReentrenamiento completo. Ahora puedes ejecutar server.py sin las advertencias de versión.")