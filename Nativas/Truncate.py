from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Instrucciones.Funcion import Funcion
import math

class Truncate(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre =nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    def interpretar(self, tree, table):
        simbolo = table.getTabla("truncate##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de Truncate", self.fila, self.columna)
        
        if simbolo.getTipo() != TIPO.DECIMAL:
            return Excepcion("Semantico", "Tipo de parametro de Truncate no es un valor numerico.", self.fila, self.columna)
        valor = self.truncate(simbolo.getValor(),0)
        self.tipo = TIPO.ENTERO
        return valor
    
    def truncate(self,number, decimals=0):
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer.")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more.")
        elif decimals == 0:
            return math.trunc(number)

        factor = 10.0 ** decimals
        return math.trunc(number * factor) / factor
    def getNodo(self):
        nodo = NodoAST("TRUNCATE")
        return nodo