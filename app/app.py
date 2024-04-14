# app/app.py

import tkinter as tk
from src.gui.menu import SeleccionAnimal

def main():
    root = tk.Tk()
    root.withdraw()
    app = SeleccionAnimal(root)
    app.mainloop()

if __name__ == "__main__":
    main()
