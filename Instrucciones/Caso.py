from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Caso(Instruccion):
    def __init__(self, expresion,instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table,valor):
        value = self.expresion.interpretar(tree,table)
        if value == valor:
            nuevaTabla = TablaSimbolos(table) 
            for instruccion in self.instrucciones:      # REALIZAR LAS ACCIONES
                value = instruccion.interpretar(tree,nuevaTabla)
                if isinstance(value, Excepcion) :
                    tree.getExcepciones().append(value)
                    tree.updateConsola(value.toString())
                if isinstance(value, Break): 
                    return value
        
        