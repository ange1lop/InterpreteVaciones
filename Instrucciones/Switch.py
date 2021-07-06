from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
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
                if isinstance(result, Continue): return result
                if isinstance(result, Return): return result
        
        if self.defecto != None:
            result = self.defecto.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL DEFAULT
            if isinstance(result, Break): return None
    
    def getNodo(self):
        nodo = NodoAST("SWITCH")
        codicion = NodoAST("Condicion")
        codicion.agregarHijoNodo(self.condicion.getNodo())
        nodo.agregarHijoNodo(codicion)
        instrucciones = NodoAST("CASOS")
        for instr in self.casos:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        if self.defecto != None:
            nodo.agregarHijoNodo(self.defecto.getNodo())
        return nodo  