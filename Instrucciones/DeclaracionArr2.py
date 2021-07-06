import copy
import Expresiones.Primitivos
from Abstract.Instruccion import Instruccion
from Abstract.NodoAST import NodoAST
from TS.Excepcion         import Excepcion
from TS.Simbolo           import Simbolo
from TS.TablaSimbolos import TablaSimbolos
from TS.Tipo              import *


class DeclaracionArr2(Instruccion):
    def __init__(self, tipo,corchetes,id, lst_expresion, fila, columna):
        
        self.id        = id
        self.fila      = fila
        self.columna   = columna
        self.tipo      = tipo
        self.t_esperado= tipo
        self.corchete  = corchetes
        self.lst_expresion = lst_expresion
    #1. coinciden las dimensiones que vienen con las que se esperan
    #2. comprobar si la matriz tiene la mismaa cantidad de valores en cada arreglo
    #3. comprobar el tipo
    def interpretar(self, tree, table):
        dimensiones = self.dimesiones(self.lst_expresion,0)
        arreglo = []

        if self.corchete == dimensiones:
            #crear arreglos
            value = self.crear_dimensiones(tree, table, copy.copy(self.lst_expresion),self.tipo)  # RETORNA EL ARREGLO DE DIMENSIONES
            if isinstance(value, Excepcion): return value
            simbolo = Simbolo(str(self.id), self.tipo, True,self.fila, self.columna, value)

            simbolo.arreglo = True
            # = "Ar"
            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            return None




        else:
            return Excepcion("Semantico"," No Coinciden las Dimenesiones con la cantidad de arreglos ingresados",self.fila,self.columna)

    def dimesiones(self, element, ttry):

        if isinstance(element, list):
            if isinstance(element[0], list):
                ttry += 1
                return self.dimesiones(element[0], ttry)
            else:
                return ttry

    def crear_dimensiones(self, tree, table, expresiones,tipo):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        #verificar si es una lista o una expresion, para ver si se interpreta o no
        if isinstance(dimension,list):
            cant_list = len(dimension)
            while  cant_list != 0:
                arreglo = self.crear_dimensiones(tree,table,dimension,tipo)
                arr.append(arreglo)
                cant_list -= 1
        else:
            primitivo = dimension.interpretar(tree,table)
            if self.t_esperado == dimension.tipo:
                return  primitivo
            else:
                return Excepcion("Semantico"," No se puede inferir tipo de datos en Arreglos",self.fila,self.columna)

        return arr



    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO 2")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.corchete))
        nodo.agregarHijo(str(self.id))
        nodo.agregarHijo(str(self.t_esperado))
        return nodo
