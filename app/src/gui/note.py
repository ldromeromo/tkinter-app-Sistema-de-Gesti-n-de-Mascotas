# app/src/gui/note.py

import tkinter as tk
from tkinter import messagebox
from ..logic import guardar_datos, consultar
import datetime  # Importamos datetime para manejar las fechas y horas
import os

class Aplicacion(tk.Toplevel):
    def __init__(self, parent, animal_nombre, animales):
        super().__init__(parent)
        self.animal_nombre = animal_nombre
        self.animales = animales
        self.animal = next((a for a in self.animales if a['nombre'] == self.animal_nombre), None)
        self.title(f"Tareas para {self.animal_nombre}")
        self._crear_widgets()

    def _crear_widgets(self):
        # Configurar la grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Listbox para mostrar las tareas
        self.lista_tareas = tk.Listbox(self, height=10, width=50)
        self.lista_tareas.grid(row=0, column=0, rowspan=4, padx=10, pady=20, sticky="nsew")

        # Carga las tareas existentes en el Listbox
        for tarea in self.animal['notas']:
            self.lista_tareas.insert(tk.END, tarea)

        # Entrada para nuevas tareas
        self.entrada_tarea = tk.Entry(self, width=40)
        self.entrada_tarea.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botón para agregar tareas
        boton_agregar = tk.Button(self, text="Agregar nota", command=self._agregar_tarea)
        boton_agregar.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Botón para eliminar tareas
        boton_eliminar = tk.Button(self, text="Eliminar nota", command=self._eliminar_tarea)
        boton_eliminar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        boton_exportar = tk.Button(self, text="Exportar Notas", command=self._exportar_notas)
        boton_exportar.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def _agregar_tarea(self):
        tarea = self.entrada_tarea.get().strip()
        if tarea:
            # Obtener la fecha y hora actual
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            # Formatear la tarea con la fecha y hora
            tarea_con_fecha = f"{timestamp}: {tarea}"
            self.lista_tareas.insert(tk.END, tarea_con_fecha)
            self.animal['notas'].append(tarea_con_fecha)
            guardar_datos(self.animales)
            self.entrada_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "La tarea no puede estar vacía.")

    def _eliminar_tarea(self):
        seleccionado = self.lista_tareas.curselection()
        if seleccionado:
            self.lista_tareas.delete(seleccionado[0])
            self.animal['notas'].pop(seleccionado[0])
            guardar_datos(self.animales)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una nota para eliminar.")
            
    def _exportar_notas(self):
        body, response = consultar(f"export-notas/{self.animal_nombre}")
        if body.get('success'):
            messagebox.showinfo("Éxito", body.get('message'))
        else:
            messagebox.showerror("Error", "No se pudo exportar las notas: " + body.get("error", ""))

            