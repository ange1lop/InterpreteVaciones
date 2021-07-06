from Abstract.NodoAST import NodoAST
from tkinter import *
import sys
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO

class Read(Instruccion):
    def __init__(self, raiz,consola, fila, columna):
        self.raiz = raiz
        self.fila = fila
        self.consola = consola
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        print("Ingreso a un READ. Ingrese el valor")
        print(self.consola)
        # ESTO SOLO ES DE EJEMPLO
        self.consola.delete(1.0, END)
        self.consola.insert(INSERT, tree.getConsola())
        string = CustomDialog(self.raiz, "Enter something:").show()
        print(string)
        return string
    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo

class CustomDialog(Toplevel):
    def __init__(self, parent, prompt):
        Toplevel.__init__(self, parent)

        self.var = StringVar()

        self.label = Label(self, text=prompt)
        self.entry = Entry(self, textvariable=self.var)
        self.ok_button = Button(self, text="OK", command=self.on_ok)

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x")
        self.ok_button.pack(side="right")

        self.entry.bind("<Return>", self.on_ok)

    def on_ok(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.entry.focus_force()
        self.wait_window()
        return self.var.get()