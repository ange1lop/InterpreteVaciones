from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre.lower()) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: " + self.nombre, self.fila, self.columna)
        nuevaTabla = TablaSimbolos(tree.getTSGlobal())
        # OBTENER PARAMETROS
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Excepcion): return resultExpresion
                print("Entre a llamada")
                print(result.parametros[contador]["tipo"])
                print(expresion.tipo)
                if result.parametros[contador]["tipo"] == expresion.tipo:  # VERIFICACION DE TIPO
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    
                    if result.parametros[contador]['lista']:
                        if not expresion.arreglo: 
                            return Excepcion("Semantico", "un parametro no es un arreglo.", self.fila, self.columna)
                        
                        dim = self.dimesiones(resultExpresion,1)
                        if result.parametros[contador]['dimension'] != dim:   #VERIFICACION DE DIMENSIONES
                            return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipo'], True,self.fila, self.columna, resultExpresion)

                        resultTabla = nuevaTabla.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipo'], False,self.fila, self.columna, resultExpresion)

                        resultTabla = nuevaTabla.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla
                elif self.nombre.lower() == "truncate" and (expresion.tipo == TIPO.DECIMAL or expresion.tipo == TIPO.ENTERO):
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipo'], False, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                elif self.nombre.lower() == "typeof":
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), expresion.tipo, expresion.arreglo, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                elif self.nombre.lower() == "length":
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), expresion.tipo, expresion.arreglo, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna)
                contador += 1

            
        else: 
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
    
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Excepcion): return value
        self.tipo = result.tipo
        
        return value
    def dimesiones(self, element, ttry):

        if isinstance(element, list):
            if isinstance(element[0], list):
                ttry += 1
                return self.dimesiones(element[0], ttry)
            else:
                return ttry
    
    def getNodo(self):
        nodo = NodoAST("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo 