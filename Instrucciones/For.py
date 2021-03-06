from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Asignacion import Asignacion

class For(Instruccion):
    def __init__(self, variable ,condicion, actualizar, instrucciones, fila, columna):
        self.variable = variable
        self.actualizar = actualizar
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = None
        valor = None
        obtener = False
        declarar = True
        if isinstance(self.variable, Asignacion) :
            obtener = False
            declarar = False
            valor = self.variable.interpretar(tree,table)
        while True:
            nuevaTabla = TablaSimbolos(table) 
            nuevaTabla.ambito = table.ambito +"For"
            if obtener: 
                nuevaTabla.setTabla(simbolo)
            if declarar : 
                valor = self.variable.interpretar(tree,nuevaTabla)
                declarar = False
                obtener = True
            if isinstance(valor, Excepcion): return valor
            condicion = self.condicion.interpretar(tree, nuevaTabla)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                          #NUEVO ENTORNO
                    
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Continue): pass
                    acres = self.actualizar.interpretar(tree,nuevaTabla)
                    if isinstance(acres, Excepcion): return acres
                    simbolo = nuevaTabla.getTabla(self.variable.identificador.lower())
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en condicion for.", self.fila, self.columna)
    def getNodo(self):
        nodo = NodoAST("FOR")
        variable = NodoAST("Variable")
        variable.agregarHijoNodo(self.variable.getNodo())
        nodo.agregarHijoNodo(variable)
        codicion = NodoAST("Condicion")
        codicion.agregarHijoNodo(self.condicion.getNodo())
        nodo.agregarHijoNodo(codicion)
        increm = NodoAST("Incremento")
        increm.agregarHijoNodo(self.actualizar.getNodo())
        nodo.agregarHijoNodo(increm)
        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo 