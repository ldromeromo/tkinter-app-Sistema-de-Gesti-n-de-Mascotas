#   Api/src/logic.py

def calcular_peso_ideal(animal, edad):
    if animal.lower() == "perro":
        return 10 * min(edad, 10) + 5 if edad <= 10 else 105
    elif animal.lower() == "gato":
        return 4 * edad + 2
    elif animal.lower() == "conejo":
        return 2 * edad + 0.5
    elif animal.lower() == "vaca":
        return 100 * edad + 200
    elif animal.lower() == "loro":
        return 0.2 * edad + 0.5
    elif animal.lower() == "tortuga":
        return 1 * edad + 1
    elif animal.lower() == "caballo":
        return 50 * edad + 100
    else:
        return "Animal no reconocido"