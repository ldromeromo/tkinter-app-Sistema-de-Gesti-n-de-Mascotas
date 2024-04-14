# app/src/gui/menu.py

import tkinter as tk
from tkinter import messagebox
from ..logic import cargar_datos, guardar_datos, consultar

class DetalleMascota(tk.Toplevel):
    def __init__(self, parent, animal_index, animales):
        super().__init__(parent)
        self.animal_index = animal_index
        self.animales = animales
        self.animal = self.animales[animal_index] 
        self.title(f"Detalles de {self.animal['nombre']}")
        self._crear_widgets()
        self._actualizar_detalles()
        
    def _crear_widgets(self):
        self.grid_columnconfigure(1, weight=1)  

        tk.Label(self, text="Peso (kg):").grid(row=0, column=1, sticky="e")
        self.entry_peso = tk.Entry(self)
        self.entry_peso.insert(0, self.animal.get('peso', ''))
        self.entry_peso.grid(row=0, column=2, padx=20, pady=(0, 5), sticky="ew")

        tk.Label(self, text="Enfermedades:").grid(row=1, column=1, sticky="e")
        self.entry_enfermedades = tk.Entry(self)
        self.entry_enfermedades.insert(0, self.animal.get('enfermedades', ''))
        self.entry_enfermedades.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="ew")

        tk.Button(self, text="Guardar", command=self._guardar_datos).grid(row=3, column=1, columnspan=2, pady=10, sticky="ew")

        tk.Label(self, text="Peso ideal:").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.label_peso_ideal = tk.Label(self, text="Calculando...")
        self.label_peso_ideal.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Estado de peso:").grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.label_estado_peso = tk.Label(self, text="Calculando...")
        self.label_estado_peso.grid(row=1, column=4, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Comida recomendada:").grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.label_comida = tk.Label(self, text="Calculando...")
        self.label_comida.grid(row=2, column=4, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Comida no recomendada:").grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.label_evitar = tk.Label(self, text="Calculando...")
        self.label_evitar.grid(row=3, column=4, padx=10, pady=5, sticky="w")

    def _actualizar_detalles(self):
        if not self.animal.get('peso') or not self.animal.get('edad'):
            self.label_peso_ideal.config(text="Datos faltantes")
            self.label_estado_peso.config(text="Datos faltantes")
            self.label_comida.config(text="Datos faltantes")
            self.label_evitar.config(text="Datos faltantes")
            return

        peso_actual = float(self.animal.get('peso', 1))
        edad = self.animal.get('edad', 1)
        tipo_animal = self.animal['tipo']
        
        params = {"tipo_animal": tipo_animal, "peso": peso_actual, "edad": edad}
        response, status = consultar("recomendacion", params)
        
        if status.status_code == 200:
            self.label_peso_ideal.config(text=f"{response['peso_ideal']} kg")
            self.label_estado_peso.config(text=response['estado_peso'])
            self.label_comida.config(text=response['comida'])
            self.label_evitar.config(text=response['evitar'])
        else:
            self.label_peso_ideal.config(text="No disponible")
            self.label_estado_peso.config(text="No disponible")
            self.label_comida.config(text="No disponible")
            self.label_evitar.config(text="No disponible")
            
    def _guardar_datos(self):
        self.animal['peso'] = self.entry_peso.get()
        self.animal['enfermedades'] = self.entry_enfermedades.get()
        self.animales[self.animal_index] = self.animal 
        guardar_datos(self.animales)
        self._actualizar_detalles()
        
    def _ver_detalles(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            animal_nombre = item['values'][0]
            animal_index = next((index for index, a in enumerate(self.animales) if a['nombre'] == animal_nombre), None)
            if animal_index is not None:
                ventana_detalles = DetalleMascota(self, animal_index, self.animales)
                ventana_detalles.grab_set()
            else:
                messagebox.showerror("Error", "Animal not found.")
        else:
            messagebox.showwarning("Warning", "Please select an animal.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    animales = cargar_datos()
    app = DetalleMascota(root, 0, animales)
    app.mainloop()