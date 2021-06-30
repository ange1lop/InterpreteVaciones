from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class Switch(Instruccion):
    def __init__(self, condicion, casos,defecto, fila, columna):
        self.condicion = condicion
        self.casos = casos
        self.defecto = defecto
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion
        
        for instruccion in self.casos:
            if True:
                result = instruccion.interpretar(tree, table,condicion) #EJECUTA INSTRUCCION ADENTRO DEL CASE
                if isinstance(result, Excepcion) :
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                if isinstance(result, Break): return None
        
        if self.defecto != None:
            result = self.defecto.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL DEFAULT
            if isinstance(result, Break): return None