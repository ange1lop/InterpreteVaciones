from re import A
from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy


class Referencia(Instruccion):
    def __init__(self, tipo, dimensiones_array1, identificador1, identificador2, fila, columna):
        self.identificador1 = identificador1
        self.identificador2 = identificador2
        self.tipo = tipo
        self.dimensiones_array1 = dimensiones_array1
        self.fila = fila
        self.columna = columna
        self.arreglo = True
        self.dimensiones_array2 = 1


    def interpretar(self, tree, table):
        try:
            array2 = table.getTabla(self.identificador2.lower())
            
            if array2 == None:
                return Excepcion("Semantico", "Variable " + self.identificador2 + " no encontrada.", self.fila, self.columna)

            if not array2.getArreglo(): 
                return Excepcion("Semantico", "Variable " + self.identificador2 + " no es un arreglo.", self.fila, self.columna)

            if self.tipo != array2.getTipo():
                return Excepcion("Semantico", "Tipo de dato diferente en " + self.identificador2, self.fila, self.columna)
            
            expresiones_array2 = array2.getValor()
            self.obtenerDimension(expresiones_array2)
            dim = self.dimesiones(expresiones_array2,1)
            print("Dimensiones Array 1: "+str(self.dimensiones_array1))
            print("Dimensiones Array 2:"+str(dim))
            if self.dimensiones_array1 != dim:   #VERIFICACION DE DIMENSIONES
                return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)
            print(str(self.identificador1))
            result = table.setTabla2(array2,str(self.identificador1))
            if isinstance(result, Excepcion): return result
            return None
        except:
            return Excepcion("Semantico", "El indice del array sobrepasa el rango.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("REFERENCIA ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.dimensiones_array1))
        nodo.agregarHijo(str(self.identificador1))
        nodo.agregarHijo(str(self.identificador2))
        return nodo

    def dimesiones(self, element, ttry):

        if isinstance(element, list):
            if isinstance(element[0], list):
                ttry += 1
                return self.dimesiones(element[0], ttry)
            else:
                return ttry
    def obtenerDimension(self, expresiones):#puacMethod
        for expresion in expresiones:
            if(isinstance(expresion,list)):
                self.dimensiones_array2 += 1 
                self.obtenerDimension(expresion)
            return None