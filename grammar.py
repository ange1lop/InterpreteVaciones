''' 
Angel Lopez 
VACACIONES DE JUNIO

Proyecto
'''
from Instrucciones.DeclaracionArr2 import DeclaracionArr2
from Instrucciones.Referencia import Referencia
from tkinter.constants import N
from Abstract.NodoAST import NodoAST
from Nativas.Typeof import Typeof
import re
from TS.Excepcion import Excepcion

errores = []
principal = None
console = None
reservadas = {
    'int'       : 'RINT',
    'double'     : 'RFLOAT',
    'string'    : 'RSTRING',
    'boolean'   : 'RBOOLEAN',
    'char'      : 'RCHAR',
    'print'     : 'RPRINT',
    'if'        : 'RIF',
    'switch'    : 'RSWITCH',
    'case'      : 'RCASE',
    'default'   : 'RDEFAULT',
    'for'       : 'RFOR',
    'else'      : 'RELSE',
    'while'     : 'RWHILE',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'break'     : 'RBREAK',
    'main'      : 'RMAIN',
    'func'      : 'RFUNC',
    'null'      : 'RNULL',
    'var'       : 'RVAR',
    'return'    : 'RRETURN',
    'continue'  : 'RCONTINUE',
    'read'      : 'RREAD',
    'new'       : 'RNEW',
}

tokens  = [
    'PUNTOCOMA',
    'DOSPUNTO',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'MASMAS',
    'MENOSMENOS',
    'MAS',
    'MENOS',
    'POTENCIA',
    'MULTI',
    'CORA',
    'CORC',
    'DIV',
    'MOD',
    'MENORQUE',
    'MAYORQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'IGUAL',
    'AND',
    'OR',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_DOSPUNTO      = r':'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_COMA          = r','
t_MASMAS        = r'\+\+'
t_MENOSMENOS    = r'\-\-'
t_MAS           = r'\+'
t_POTENCIA      = r'\*\*'
t_CORA          = r'\['
t_CORC          = r'\]'
t_MOD           = r'%'
t_MULTI         = r'\*' 
t_DIV           = r'/'
t_MENOS         = r'-'
t_MENORIGUAL      = r'<='
t_MAYORIGUAL      = r'>='
t_MENORQUE      = r'<'
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_DIFERENTE    = r'=!'
t_IGUAL         = r'='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CARACTER(t):
    r"""\'(\\'|\\\\|\\n|\\t|\\r|\\"|[^\\\'\"])?\'"""
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\t','\t')
    t.value = t.value.replace('\\n','\n')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\"',"\"")
    t.value = t.value.replace('\\\\','\\')
    return t


def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t):
    r'\"(\\"|.)*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace("\\t","\t")
    t.value = t.value.replace("\\n","\n")
    t.value = t.value.replace('\\"',"\"")
    t.value = t.value.replace('\\\\','\\')
    return t


# Comentario simple // ...
def t_COMENTARIO_MULTILINEA(t):
    r'\#\*(.|\n)*\*\#'
    cantida = t.value.split('\n')
    t.lexer.lineno += (len(cantida)-1)

def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error l??xico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador l??xico
import ply.lex as lex
lexer = lex.lex(reflags= re.IGNORECASE)

# Asociaci??n de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    ('left','MENORQUE','MAYORQUE', 'IGUALIGUAL','MENORIGUAL','MAYORIGUAL','DIFERENTE'),
    ('left','MAS','MENOS'),
    ('left','DIV','MULTI','MOD'),
    ('left','POTENCIA'),
    ('right','UMENOS'),
    )

# Definici??n de la gram??tica

#Abstract
from Abstract.Instruccion import Instruccion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivos import Primitivos
from TS.Tipo import OperadorAritmetico, OperadorLogico, TIPO, OperadorRelacional
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Instrucciones.Declaracion import Declaracion
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.Switch import Switch
from Instrucciones.Caso import Caso
from Instrucciones.Defecto import Defecto
from Instrucciones.Break import Break
from Instrucciones.Main import Main
from Instrucciones.Funcion import Funcion
from Instrucciones.Llamada import Llamada
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Expresiones.Read import Read
from Nativas.ToUpper import ToUpper
from Nativas.ToLower import ToLower
from Nativas.Truncate import Truncate
from Nativas.Round import Round
from Nativas.Length import Length
from Expresiones.Casteo import Casteo
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Expresiones.AccesoArreglo import AccesoArreglo
from Instrucciones.ModificarArreglo import ModificarArreglo

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr finins
                        | declaracion_instr finins
                        | asignacion_instr finins
                        | incremento_instr finins
                        | if_instr
                        | while_instr
                        | for_instr
                        | break_instr finins
                        | main_instr
                        | funcion_instr
                        | llamada_instr finins
                        | switch_instr
                        | return_instr  finins
                        | continue_instr  finins
                        | declArr_instr finins
                        | modArr_instr finins'''
    t[0] = t[1]

def p_finins(t) :
    '''finins       : PUNTOCOMA
                    | '''
    t[0] = None

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sint??ctico","Error Sint??ctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////DECLARACION//////////////////////////////////////////////////

def p_declaracion(t) :
    'declaracion_instr     : RVAR ID IGUAL expresion'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])

def p_declaracion_nula(t) :
    'declaracion_instr     : RVAR ID'
    t[0] = Declaracion( t[2], t.lineno(2), find_column(input, t.slice[2]), None)

#///////////////////////////////////////DECLARACION ARREGLOS//////////////////////////////////////////////////

def p_declArr(t) :
    '''declArr_instr     : tipo1
                        | tipo2
                        | array_referencia'''
    t[0] = t[1]

def p_tipo1(t) :
    '''tipo1     : tipo lista_Dim ID IGUAL RNEW tipo lista_expresiones'''
    t[0] = DeclaracionArr1(t[1], t[2], t[3], t[6], t[7], t.lineno(3), find_column(input, t.slice[3]))

def p_lista_Dim1(t) :
    'lista_Dim     : lista_Dim CORA CORC'
    t[0] = t[1] + 1

def p_lista_Dim2(t) :
    'lista_Dim    : CORA CORC'
    t[0] = 1

def p_lista_expresiones_1(t) :
    'lista_expresiones     : lista_expresiones CORA expresion CORC'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_expresiones_2(t) :
    'lista_expresiones    : CORA expresion CORC'
    t[0] = [t[2]]

def p_arrayReferencia(t):
    'array_referencia   : tipo lista_Dim ID IGUAL ID'
    t[0] = Referencia(t[1],t[2],t[3],t[5],t.lineno(3), find_column(input, t.slice[3]))

#tipo 2

def p_tipo2(t):
    """
    tipo2 : tipo lista_Dim ID IGUAL lst_values
    """
    t[0] = DeclaracionArr2(t[1],t[2],t[3],t[5],t.lineno(4), find_column(input, t.slice[4]))

########################################################################################################
def p_lst_values(t) :
    '''lst_values    :  lst_values COMA LLAVEA value LLAVEC
    '''
    if t[4] != "":
        t[1].append(t[4])
    t[0] = t[1]

def p_lst_value(t) :
    '''lst_values    : LLAVEA value LLAVEC
    '''
    if t[2] == "":
        t[0] = []
    else:
        t[0] = [t[2]]

def p_value(t):
    """
    value :  lst_values
            | lst_expresion
    """
    t[0] = t[1]

#************************#
def p_lst_values_expresio(t) :
    '''lst_expresion    : lst_expresion COMA expresion
    '''
    if t[3] != "":
        t[1].append(t[3])
    t[0] = t[1]

def p_lst_value_expresion_final(t) :
    '''lst_expresion    : expresion
    '''
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

#///////////////////////////////////////MODIFICACION ARREGLOS//////////////////////////////////////////////////


def p_modArr(t) :
    '''modArr_instr     :  ID lista_expresiones IGUAL expresion'''
    t[0] = ModificarArreglo(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_return(t) :
    'return_instr     : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t) :
    'asignacion_instr     : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_incremento(t) :
    'incremento_instr      : ID MASMAS'
    o1 = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))
    sus= Primitivos(TIPO.ENTERO,1, t.lineno(2), find_column(input, t.slice[2]))
    res = Aritmetica(OperadorAritmetico.MAS, o1,sus, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = Asignacion(t[1], res, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_decremento(t) :
    'incremento_instr     : ID MENOSMENOS'
    o1 = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))
    sus= Primitivos(TIPO.ENTERO,1, t.lineno(2), find_column(input, t.slice[2]))
    res = Aritmetica(OperadorAritmetico.MENOS, o1,sus, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = Asignacion(t[1], res, t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////IF//////////////////////////////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


#//////////////////////////////////////SWITCH/////////////////////////////////////////////////
def p_switch1(t):
    'switch_instr : RSWITCH PARA expresion PARC LLAVEA casos default  LLAVEC'
    t[0] = Switch(t[3], t[6], t[7],t.lineno(1), find_column(input, t.slice[1]))


def p_switch2(t):
    'switch_instr : RSWITCH PARA expresion PARC LLAVEA casos LLAVEC'
    print(len(t[6]))
    t[0] = Switch(t[3], t[6], None,t.lineno(1), find_column(input, t.slice[1]))

def p_switch3(t):
    'switch_instr : RSWITCH PARA expresion PARC LLAVEA default  LLAVEC'
    t[0] = Switch(t[3], None, t[6],t.lineno(1), find_column(input, t.slice[1]))

def p_lista_casos(t) :
    'casos    : casos caso'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_lista_caso(t) :
    'casos    : caso'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

def p_caso(t):
    'caso       : RCASE expresion DOSPUNTO instrucciones'
    t[0] = Caso(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_default(t):
    'default       : RDEFAULT DOSPUNTO instrucciones'
    t[0] = Defecto(t[3], t.lineno(1), find_column(input, t.slice[1]))
    
#///////////////////////////////////////FOR//////////////////////////////////////////////////

def p_for(t) :
    'for_instr     : RFOR  PARA fvariable PUNTOCOMA expresion PUNTOCOMA actualizar PARC LLAVEA instrucciones LLAVEC'
    t[0] = For(t[3], t[5], t[7],t[10],t.lineno(1), find_column(input, t.slice[1]))

def p_for_variable(t):
    '''fvariable    : declaracion_instr
                    | asignacion_instr
                    '''
    t[0] = t[1]

def p_for_actualizar(t):
    '''actualizar    : incremento_instr
                    | asignacion_instr
                    '''
    t[0] = t[1]

#///////////////////////////////////////WHILE//////////////////////////////////////////////////

def p_while(t) :
    'while_instr     : RWHILE PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////BREAK//////////////////////////////////////////////////

def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////MAIN//////////////////////////////////////////////////

def p_main(t) :
    'main_instr     : RMAIN PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////FUNCION//////////////////////////////////////////////////

def p_funcion_1(t) :
    'funcion_instr     : RFUNC ID PARA parametros PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_2(t) :
    'funcion_instr     : RFUNC ID PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], [], t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////

def p_parametros_1(t) :
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_2(t) :
    'parametros    : parametro'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO//////////////////////////////////////////////////

def p_parametro(t) :
    'parametro     : tipo ID'
    t[0] = {'tipo':t[1],'identificador':t[2],'lista':False,'dimension':0}

def p_parametro2(t) :
    'parametro     : tipo lista_Dim ID'
    t[0] = {'tipo':t[1],'identificador':t[3],'lista':True,'dimension':t[2]}

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_llamada1(t) :
    'llamada_instr     : ID PARA PARC'
    t[0] = Llamada(t[1], [], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada2(t) :
    'llamada_instr     : ID PARA parametros_llamada PARC'
    t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametrosLL_2(t) :
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametroLL(t) :
    'parametro_llamada     : expresion'
    t[0] = t[1]

#///////////////////////////////////////TIPO//////////////////////////////////////////////////

def p_tipo(t) :
    '''tipo     : RINT
                | RFLOAT
                | RSTRING
                | RBOOLEAN
                | RCHAR 
                | RNULL '''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA
    elif t[1].lower() == 'boolean':
        t[0] = TIPO.BOOLEANO
    elif t[1].lower() == 'char':
        t[0] = TIPO.CHARACTER
    elif t[1].lower() == 'null':
        t[0] = TIPO.NULO

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_incremento(t):
    '''
    expresion : incremento_instr
    '''
    t[0] = t[1]

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion MULTI expresion
            | expresion POTENCIA expresion
            | expresion DIV expresion
            | expresion MOD expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORIGUAL expresion
            | expresion IGUALIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_caracter(t):
    '''expresion : CARACTER'''
    t[0] = Primitivos(TIPO.CHARACTER,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llamada(t):
    '''expresion : llamada_instr'''
    t[0] = t[1]

def p_expresion_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_null(t):
    '''expresion : RNULL'''
    t[0] = Primitivos(TIPO.NULO, None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cast(t):
    '''expresion : PARA tipo PARC expresion'''
    t[0] = Casteo(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_read(t):
    '''expresion : RREAD PARA PARC'''
    t[0] = Read(principal,console,t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_Arreglo(t):
    '''expresion : ID lista_expresiones'''
    t[0] = AccesoArreglo(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))


import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def crearNativas(ast):          # CREACION Y DECLARACION DE LAS FUNCIONES NATIVAS
    nombre = "toupper"
    parametros = [{'tipo':TIPO.CADENA,'identificador':'toUpper##Param1'}]
    instrucciones = []
    toUpper = ToUpper(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(toUpper)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    nombre = "tolower"
    parametros = [{'tipo':TIPO.CADENA,'identificador':'toLower##Param1'}]
    instrucciones = []
    toLower = ToLower(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(toLower)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    nombre = "truncate"
    parametros = [{'tipo':TIPO.DECIMAL,'identificador':'truncate##Param1'}]
    instrucciones = []
    truncate = Truncate(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(truncate)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    nombre = "round"
    parametros = [{'tipo':TIPO.DECIMAL,'identificador':'round##Param1'}]
    instrucciones = []
    round = Round(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(round)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    nombre = "typeof"
    parametros = [{'tipo':TIPO.NULO,'identificador':'typeof##Param1'}]
    instrucciones = []
    typeof = Typeof(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(typeof)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
    nombre = "length"
    parametros = [{'tipo':TIPO.NULO,'identificador':'toLength##Param1'}]
    instrucciones = []
    lent = Length(nombre, parametros, instrucciones, -1, -1)
    ast.addFuncion(lent)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ
from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos
def ejecutar(entrada,raiz,consola):
    global principal
    principal = raiz
    print(consola)
    global console
    console = consola
    instrucciones = parse(entrada) # ARBOL AST
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    TSGlobal.ambito = "GLOBAL"
    ast.setTSglobal(TSGlobal)
    crearNativas(ast)
    for error in errores:                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        ast.getExcepciones().append(error)
        ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones():      # 1ERA PASADA (DECLARACIONES Y ASIGNACIONES)
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
        if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, ModificarArreglo) or isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, Referencia):
            
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            if isinstance(value, Continue): 
                err = Excepcion("Semantico", "Sentencia CONTINUE fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            
    for instruccion in ast.getInstrucciones():      # 2DA PASADA (MAIN)
        contador = 0
        if isinstance(instruccion, Main):
            contador += 1
            if contador == 2: # VERIFICAR LA DUPLICIDAD
                err = Excepcion("Semantico", "Existen 2 funciones Main", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
                break
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            if isinstance(value, Continue): 
                err = Excepcion("Semantico", "Sentencia CONTINUE fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            if isinstance(value, Return): 
                err = Excepcion("Semantico", "Sentencia Return fuera de funcion con retorno", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())

    for instruccion in ast.getInstrucciones():    # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
        if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Funcion) or isinstance(instruccion, DeclaracionArr1) or isinstance(instruccion, ModificarArreglo) or isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, Referencia)):
            err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
            ast.getExcepciones().append(err)
            ast.updateConsola(err.toString())
    init = NodoAST("RAIZ")
    instr = NodoAST("INSTRUCCIONES")

    for instruccion in ast.getInstrucciones():
        instr.agregarHijoNodo(instruccion.getNodo())

    init.agregarHijoNodo(instr)
    grafo = ast.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST
    
    ast.reporteSimbolo = TSGlobal.lista
    return ast

def leer():
    
    f = open("./entrada.txt", "r",encoding="UTF-8")
    entrada = f.read()
    ast = ejecutar(entrada)
    print(ast.getConsola())

