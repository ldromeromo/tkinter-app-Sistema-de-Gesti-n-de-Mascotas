# app/src/gui/menu.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .note import Aplicacion
from .detail import DetalleMascota
from ..logic import cargar_datos, guardar_datos, consultar

class SeleccionAnimal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sistema de Gestión de Mascotas")
        self.animales = cargar_datos()
        self.tipos_animales, self.status = consultar("tipos-animales")
        self._crear_lista_animales()

    def _crear_lista_animales(self):
        self.tree = ttk.Treeview(self, columns=("Nombre", "Tipo", "Edad"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Edad", text="Edad")
        self.tree.column("Nombre", width=120)
        self.tree.column("Tipo", width=100)
        self.tree.column("Edad", width=50)
        self.tree.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

        for animal in self.animales:
            self.tree.insert("", "end", values=(animal['nombre'], animal['tipo'], animal['edad']))

        # Botonera
        botonera = tk.Frame(self)
        botonera.pack(pady=10)

        boton_seleccionar = tk.Button(botonera, text="Seleccionar", command=self._seleccionar_animal)
        boton_seleccionar.pack(side=tk.LEFT, padx=5)

        boton_agregar = tk.Button(botonera, text="Agregar Animal", command=self._agregar_animal)
        boton_agregar.pack(side=tk.LEFT, padx=5)

        boton_eliminar = tk.Button(botonera, text="Eliminar Animal", command=self._eliminar_animal)
        boton_eliminar.pack(side=tk.LEFT, padx=5)

        boton_detalle = tk.Button(botonera, text="Ver Detalles", command=self._ver_detalles)
        boton_detalle.pack(side=tk.LEFT, padx=5)
        

    def _actualizar_vista(self):
        self.tree.delete(*self.tree.get_children())
        for animal in self.animales:
            self.tree.insert("", "end", values=(animal['nombre'], animal['tipo'], animal['edad']))

    def _agregar_animal(self):
        nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del animal:")
        
        dialogo_agregar = tk.Toplevel(self)
        dialogo_agregar.title("Agregar Animal")
        tk.Label(dialogo_agregar, text="Tipo:").grid(row=0, column=0)
        combo_tipos = ttk.Combobox(dialogo_agregar, values=self.tipos_animales)
        combo_tipos.grid(row=0, column=1, padx=10, pady=10)
        combo_tipos.set("Seleccione un tipo")

        tk.Label(dialogo_agregar, text="Edad:").grid(row=1, column=0)
        entrada_edad = tk.Entry(dialogo_agregar)
        entrada_edad.grid(row=1, column=1, padx=10, pady=10)

        def confirmar_agregado():
            tipo = combo_tipos.get()
            edad = entrada_edad.get()
            if nombre and tipo != "Seleccione un tipo" and edad.isdigit():
                nuevo_animal = {'nombre': nombre, 'tipo': tipo, 'edad': int(edad), 'notas': []}
                self.animales.append(nuevo_animal)
                self.tree.insert("", "end", values=(nombre, tipo, edad))
                guardar_datos(self.animales)
                dialogo_agregar.destroy()
            else:
                messagebox.showerror("Error", "Información inválida o incompleta.")

        boton_confirmar = tk.Button(dialogo_agregar, text="Agregar", command=confirmar_agregado)
        boton_confirmar.grid(row=2, columnspan=2, pady=10)

    def _seleccionar_animal(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            animal = self.tree.item(seleccionado, "values")
            nombre_animal = animal[0]
            ventana_nota = Aplicacion(self, nombre_animal, self.animales)
            ventana_nota.grab_set()
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un animal.")

    def _ver_detalles(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            animal_nombre = item['values'][0]
            # Buscar el índice del animal en la lista de animales basado en el nombre
            animal_index = next((index for index, a in enumerate(self.animales) if a['nombre'] == animal_nombre), None)
            if animal_index is not None:
                # Aquí pasamos el índice del animal y la lista completa de animales
                ventana_detalles = DetalleMascota(self, animal_index, self.animales)
                ventana_detalles.grab_set()
            else:
                messagebox.showerror("Error", "Animal no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un animal.")

    def _eliminar_animal(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            animal_nombre = item['values'][0]
            # Actualizar la lista de animales y la vista
            self.animales = [animal for animal in self.animales if animal['nombre'] != animal_nombre]
            self._actualizar_vista()
            guardar_datos(self.animales)
            messagebox.showinfo("Éxito", "Animal eliminado con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un animal para eliminar.")