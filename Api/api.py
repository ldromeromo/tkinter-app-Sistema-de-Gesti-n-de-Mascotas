#   Api/api.py

from flask import Flask, request, jsonify, send_file, abort
from src.var import TIPOS_ANIMALES, RECOMENDACIONES
from src.logic import calcular_peso_ideal, calcular_peso_ideal
import pandas as pd
import json

app = Flask(__name__)


@app.route("/tipos-animales", methods=["GET"])
def get_tipos_animales():
    return jsonify(TIPOS_ANIMALES)

@app.route("/recomendacion", methods=["GET"])
def get_recomendacion():
    tipo_animal = request.args.get('tipo_animal')
    peso = float(request.args.get('peso', 0))
    edad = float(request.args.get('edad', 0))

    if tipo_animal in RECOMENDACIONES:
        datos = RECOMENDACIONES[tipo_animal]
        peso_ideal = calcular_peso_ideal(tipo_animal, edad)
        estado_peso = "está en sobre peso" if peso > peso_ideal else "está bajo peso" if peso < peso_ideal else "está bien"
        return jsonify({"peso_ideal": peso_ideal, "estado_peso": estado_peso, "comida": datos["comida"], "evitar": datos["evitar"]})
    else:
        return jsonify({"error": "Tipo de animal no soportado"}), 404

@app.route("/export-notas/<animal_name>", methods=["GET"])
def export_notas(animal_name):
    try:
        if '/' in animal_name or '\\' in animal_name:
            abort(400, description="Invalid animal name")

        with open('datos.json') as f:
            animales = json.load(f)
        
        animal = next((a for a in animales if a['nombre'] == animal_name), None)
        if animal:
            df = pd.DataFrame(animal['notas'], columns=['Notas'])
            filename = f"{animal_name}_notas.xlsx"
            df.to_excel(filename, index=False)
            
            return jsonify({"success": True, "message": "Notas exportadas de "+ animal_name, "filename": filename})
        else:
            return jsonify({"success": False, "error": "Animal no encontrado"}), 404

    except Exception as e:
        app.logger.error(f"Exception: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": "Internal Server Error"}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
