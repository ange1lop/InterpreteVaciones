from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Instrucciones.Funcion import Funcion

class Typeof(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre =nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    def interpretar(self, tree, table):
        simbolo = table.getTabla("typeof##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de typeof", self.fila, self.columna)
        self.tipo = TIPO.ENTERO
        
        valor = str(simbolo.getTipo())
        print(simbolo.arreglo)
        if simbolo.arreglo:
            valor += "-> Arreglo"
            print("Ingreso")
        return valor.replace("TIPO.","")
    def getNodo(self):
        nodo = NodoAST("TYPEOF")
        return nodo