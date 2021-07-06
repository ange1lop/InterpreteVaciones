from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Instrucciones.Funcion import Funcion

class Round(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre =nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.valor = None
    def interpretar(self, tree, table):
        simbolo = table.getTabla("round##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de Truncate", self.fila, self.columna)
        
        if simbolo.getTipo() != TIPO.DECIMAL:
            return Excepcion("Semantico", "Tipo de parametro de Truncate no es un valor numerico.", self.fila, self.columna)
        valor = int(round(simbolo.getValor()))
        self.tipo = TIPO.ENTERO
        self.valor = valor
        return valor
    def getNodo(self):
        nodo = NodoAST("ROUND")
        return nodo