# app/src/logic.py

import json
import requests

def guardar_datos(animales, archivo='datos.json'):
    with open(archivo, 'w') as file:
        json.dump(animales, file)

def cargar_datos(archivo='datos.json'):
    try:
        with open(archivo, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def agregar_tarea(lista_nota, tarea):
    if tarea != "":
        lista_nota.insert("end", tarea)
        return True
    return False

def eliminar_tarea(lista_nota):
    try:
        indice = lista_nota.curselection()[0]
        lista_nota.delete(indice)
        return True
    except IndexError:
        return False
    
def consultar(apuntamiento, params=""):
    url = "http://localhost:5000/"
    response = requests.get( url + apuntamiento, params=params)
    
    return response.json(), response
