from src.Nativas.Fixed import Fixed
from src.Nativas.Exponential import Exponential
from src.Nativas.String import String
from src.Nativas.Lower import Lower
from src.Nativas.Upper import Upper
from src.Nativas.Split import Split
from src.Nativas.Concat import Concat
from src.Nativas.Typeof import Typeof
from src.Nativas.Length import Length

import ply.yacc as yacc
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Expresiones.aritmetica import Aritmetica
from src.Expresiones.relacional import Relacional
from src.Expresiones.logica import Logica
from src.Expresiones.Identificador import Identificador
from src.Expresiones.primitivos import Primitivos
from src.Instrucciones.imprimir import Imprimir
from src.Instrucciones.Sentencias.If import If
from src.Instrucciones.Sentencias.While import While
from src.Instrucciones.Variables.Declaracion import DeclaracionVar
from src.Instrucciones.Variables.Asignacion import AsignacionVar
from src.Instrucciones.Arreglos.Asignacion import AsignacionArreglos
from src.Instrucciones.Funcion.Funcion import Funcion
from src.Instrucciones.Funcion.LlamadaFuncion import LlamadaFuncion
from src.Instrucciones.Sentencias.Return import Return
from src.Instrucciones.Sentencias.Continue import Continue
from src.Instrucciones.Sentencias.Break import Break
from src.Instrucciones.Structs.Struct import Struct
from src.Instrucciones.Structs.Acceso import AccesoStruct
from src.Instrucciones.Structs.Modificacion import ModificacionStruct
from src.Instrucciones.Structs.DeclareStruct import DeclareStruct
from src.Instrucciones.Sentencias.For import For
from src.Instrucciones.Arreglos.Acceso import AccesoArreglo
from src.Instrucciones.Arreglos.Modificacion import ModificacionArreglo

from src.TS.Tipo import OperadorAritmetico, OperadorLogico, OperadorRelacional
from src.TS.Excepcion import Excepcion
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
from copy import copy
import sys
sys.setrecursionlimit(10000000)

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL', ),
    ('left','MAS','MENOS'),
    ('left', 'POR', 'DIV', 'PORCENTAJE'),
    ('left','PARI', 'PARD'),
    ('nonassoc', 'POTENCIA'), 
    ('right','UMENOS'),
)


#
# ///////////////////////////////////////////////////// START GRAMATICA
start = 'init'

# ///////////////////////////////////////////////////// INICIO
def p_inicio(t):
    'init : instrucciones'
    t[0] = t[1]

# ///////////////////////////////////////////////////// INSTRUCCIONES
def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_2(t):
    'instrucciones : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

# ///////////////////////////////////////////////////// INSTRUCCIONES A EVALUAR
def p_instrucciones_evaluar(t):
    '''instruccion : imprimir PTCOMA
                    | declaracion_normal PTCOMA
                    | structs_declaration 
                    | modificacion_struct PTCOMA
                    | asignacion_normal PTCOMA
                    | condicional_if PTCOMA
                    | funcion PTCOMA
                    | llamada_funcion PTCOMA
                    | llamada_struct PTCOMA
                    | inst_return PTCOMA
                    | inst_break PTCOMA
                    | inst_continue PTCOMA
                    | inst_while PTCOMA
                    | inst_for PTCOMA
                    | modificar_arreglo PTCOMA'''
    t[0] = t[1]


    
def p_error(t):
    'instruccion : error PTCOMA'
    errores.append(Excepcion("Sintáctico", "Error sintáctico, " + str(t.value), t.lineno, t.lexer.lexpos))

#///////////////////////////////////////////////////////////FUNCIONES
def p_funcion(t):
    'funcion : RFUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_sin_parametro(t):
    'funcion : RFUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Funcion(t[2],None,t[6], t.lineno(1), find_column(input, t.slice[1]))
#///////////////////////////////////////////////////////////LLAMADA FUNCION
def p_llamada_funcion(t):
    '''llamada_funcion : ID PARI PARD
                        | ID PARI parametros_ll PARD''' 
    # (let nombre: string, let apellido: string, let edad: number)
    if len(t) == 3:
        t[0] = LlamadaFuncion(t[1],None,t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = LlamadaFuncion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_struct(t):
    '''llamada_struct : RLET ID DPUNTOS ID IGUAL LLAVEIZQ structs_ll LLAVEDER'''
    t[0] = DeclareStruct(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////ATRIBUTOS STRUCTS
def p_structs_ll(t):
    '''structs_ll : struct_ll
                  | structs_ll COMA struct_ll'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

#///////////////////////////////////////////////////////////ATRIBUTO STRUCT
def p_struct_ll(t):
    'struct_ll : ID DPUNTOS expresion'
    t[0] = {'identificador' : t[1], 'parametro' : t[3]}

def p_expresion_llaves(t):
    'expresion : LLAVEIZQ structs_ll LLAVEDER'
    t[0] = t[2]

#///////////////////////////////////////////////////////////PARAMETROS DE FUNCION
def p_parametros(t):
    'parametros : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametros_2(t):
    'parametros : parametro'
    t[0] = [t[1]]

#///////////////////////////////////////////////////////////PARAMETRO DE FUNCION
def p_parametro(t):
    '''parametro : RLET ID DPUNTOS tipo  
                | ID DPUNTOS tipo
                | ID'''
    if len(t) == 2:
        t[0] = {'tipo': 'any', 'identificador': t[1]}
    elif len(t) == 4:
        t[0] = {'tipo': t[3], 'identificador': t[1]}
    else:
        t[0] = {'tipo': t[4], 'identificador': t[2]}

#///////////////////////////////////////////////////////////PARAMETROS LLAMADA FUNCION
def p_parametros_ll(t):
    'parametros_ll : parametros_ll COMA parametro_ll'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametros_ll_2(t):
    'parametros_ll : parametro_ll'
    t[0] = [t[1]]

def p_parametro_ll(t):
    '''parametro_ll : expresion'''
    t[0] = t[1]

# ///////////////////////////////////////////////////// IMPRIMIR
def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARI parametros_ll PARD'
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))

# ///////////////////////////////////////////////////// DECLARACION VARIABLES
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    t[0] = DeclaracionVar(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo(t):
    'declaracion_normal : RLET ID IGUAL expresion'
    t[0] = DeclaracionVar(t[2], 'any', t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_array(t):
    'declaracion_normal : RLET ID IGUAL CORCHETEIZQ parametros_ll CORCHETEDER'
    t[0] = DeclaracionVar(t[2], 'array', t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo_sin_valor(t):
    'declaracion_normal : RLET ID'
    t[0] = DeclaracionVar(t[2], 'any', None, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_valor(t):
    'declaracion_normal : RLET ID DPUNTOS tipo'
    if t[4] == "number":
        variable = Primitivos('number', int("0"), t.lineno(2), find_column(input, t.slice[2]))
        t[0] = DeclaracionVar(t[2], t[4], variable, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "string":
        variable = Primitivos('string', str(""), t.lineno(2), find_column(input, t.slice[2]))
        t[0] = DeclaracionVar(t[2], t[4], variable, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "boolean":
        variable = Primitivos('boolean', True, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = DeclaracionVar(t[2], t[4], variable, t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////ASIGNACION DE VARIABLES
def p_asignacion_var_tipo(t):
    'asignacion_normal : ID IGUAL expresion DPUNTOS DPUNTOS tipo'
    t[0] = AsignacionVar(t[1], t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_var(t):
    'asignacion_normal : ID IGUAL expresion'
    if isinstance(t[3], list):
        t[0] = AsignacionArreglos(t[1], t[3], 'array', t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = AsignacionVar(t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))    

#///////////////////////////////////////////////////////////MODIFICAR ARREGLO
def p_modificar_arreglo(t):
    'modificar_arreglo : ID lista_dimensiones IGUAL expresion'
    t[0] = ModificacionArreglo(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////ACCESO ARREGLO
def p_acceso_arreglo(t):
    'acceso_arreglo : ID lista_dimensiones'
    t[0] = AccesoArreglo(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))
 
def p_lista_dimensiones(t):
    'lista_dimensiones : lista_dimensiones CORCHETEIZQ expresion CORCHETEDER' 
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_dimension(t):
    'lista_dimensiones : CORCHETEIZQ expresion CORCHETEDER'
    t[0] = [t[2]] 

def p_lista_dimension_exp(t):
    'expresion : CORCHETEIZQ parametros_ll CORCHETEDER'
    t[0] = t[2] 

#///////////////////////////////////////////////////////////SENTENCIAS DE TRANSFERENCIA
def p_return_expresion(t):
    'inst_return : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_return_structs(t):
    'inst_return : RRETURN LLAVEIZQ parametros_ll LLAVEDER'
    t[0] = Return(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_return(t):
    'inst_return : RRETURN'
    t[0] = Return(None, t.lineno(1), find_column(input, t.slice[1]))

def p_sentencia_transferencia_break(t):
    'inst_break : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

def p_sentencia_transferencia_continue(t):
    'inst_continue : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

# ///////////////////////////////////////////////////// IF CONDICIONAL
def p_condicional_if(t):
    'condicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_elseif_else(t):
    'condicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifs RELSE LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[3], t[6], t[11], t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_elseif(t):
    'condicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifs'
    t[0] = If(t[3], t[6], None, t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_else(t):
    'condicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_elseifs_elseifs_elseif(t):
    'condicional_elseifs : condicional_elseifs condicional_elseif'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1] 

def p_elseifs_elseif(t):
    'condicional_elseifs : condicional_elseif'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]] 

def p_condicional_elseif(t):
    'condicional_elseif : RELSE RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[4], t[7], None, None, t.lineno(1), find_column(input, t.slice[1]))

# ///////////////////////////////////////////////////// CICLO WHILE
def p_inst_while(t):
    'inst_while : WHILE PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////FOR
def p_for_string(t): #Lo hace con strings
    'inst_for : RFOR PARI declaracion_normal ROF expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = For(t[3], t[5], None, t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_for_arrays(t): #Lo hace con arrays
    'inst_for : RFOR PARI declaracion_normal ROF CORCHETEIZQ parametros_ll CORCHETEDER PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = For(t[3], t[6], None, t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_inst_for(t):
    'inst_for : RFOR PARI  declaracion_normal PTCOMA expresion PTCOMA expresion  PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

# ///////////////////////////////////////////////////// TIPOS
def p_tipo(t):
    '''tipo : STRING
            | NUMBER
            | BOOLEAN
            | ANY CORCHETEIZQ CORCHETEDER
            | ANY CORCHETEIZQ CORCHETEDER CORCHETEIZQ CORCHETEDER
            | ID'''
    t[0] = t[1]

# ///////////////////////////////////////////////////// ARITMETICAS
def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion POTENCIA expresion
                | expresion PORCENTAJE expresion'''
    if t[2] == '+'  : 
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(OperadorAritmetico.ASTERISCO, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(OperadorAritmetico.DIVISION, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':
        t[0] = Aritmetica(OperadorAritmetico.POTENCIA, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.PORCENTAJE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_binaria_relacional(t):
    '''expresion : expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion'''
    
    if t[2] == '===':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!==':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENOR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYOR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_binaria_logica(t):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''

    if t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    '''expresion : NOT expresion %prec UNOT
                 | MENOS expresion %prec UMENOS'''

    if t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_parentesis(t):
    'expresion : PARI expresion PARD'
    t[0] = t[2]

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivos('number', int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos('number', float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivos('string', str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivos('boolean', True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos('boolean', False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_identificador(t):
    'expresion : ID'
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_llamada_funcion(t):
    'expresion : llamada_funcion'
    t[0] = t[1]

def p_expresion_llamada_struct(t):
    'expresion : llamada_struct'
    t[0] = t[1]

def p_expresion_incrementable(t):
    '''expresion : expresion MAS MAS
                 | expresion MENOS MENOS'''
    if t[2] == '+':
        incrementar = Primitivos('number', 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1], incrementar, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        decrementar = Primitivos('number', 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Primitivos(t[1], t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1], decrementar, t.lineno(2), find_column(input, t.slice[2]))

def p_acceso_struct_expresion(t):
    'expresion : acceso_struct'
    t[0] = t[1]

def p_acceso_arreglo_expresion(t):
    'expresion : acceso_arreglo'
    t[0] = t[1]

#///////////////////////////////////////////////////////////STRUCTS
def p_structs(t):
    'structs_declaration : RSTRUCT ID LLAVEIZQ lista_atributos LLAVEDER'
    t[0] = Struct(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////ATRIBUTOS
def p_atributos_atributos(t):
    'lista_atributos : lista_atributos atributo PTCOMA'
    t[1].append(t[2])
    t[0] = t[1] 

def p_atributos(t):
    'lista_atributos : atributo PTCOMA'
    t[0] = [t[1]]

#///////////////////////////////////////////////////////////ATRIBUTO
def p_atributo_tipo(t):
    'atributo : ID DPUNTOS tipo'
    t[0] = {'tipo' : t[3],'identificador' : t[1]}

def p_atributo(t):
    'atributo : ID'
    t[0] = {'tipo' : 'any','identificador' : t[1]}

#///////////////////////////////////////////////////////////ACCESO STRUCT
def p_acceso_struct(t):
    'acceso_struct : ID PUNTO ID'
    t[0] = AccesoStruct(t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_acceso_struct_2(t):
    'acceso_struct : ID PUNTO ID PUNTO ID'
    t[0] = AccesoStruct(t[1], t[5], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////MODIFICACION STRUCT
def p_modificacion_struct(t):
    'modificacion_struct : ID PUNTO ID IGUAL expresion'
    t[0] = ModificacionStruct(t[1], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))


#//////////////////////////////////////////NATIVAS
def p_to_lowercase(t):
    'expresion : ID PUNTO LWCASE PARI PARD'
    instrucciones = []
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Lower(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_uppercase(t):
    'expresion : ID PUNTO UPCASE PARI PARD'
    instrucciones = []
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Upper(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_fixed(t):
    'expresion : ID PUNTO RFIXED PARI expresion PARD'
    instrucciones = t[5]
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Fixed(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_exponential(t):
    'expresion : ID PUNTO REXP PARI expresion PARD'
    instrucciones = t[5]
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Exponential(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_string(t):
    'expresion : ID PUNTO RSTRING PARI PARD'
    instrucciones = []
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = String(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_split(t):
    'expresion : ID PUNTO RSPLIT PARI expresion PARD'
    instrucciones = t[5]
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Split(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))

def p_to_concat(t):
    'expresion : ID PUNTO RCONCAT PARI expresion PARD'
    instrucciones = t[5]
    parametro = [{'tipo':'any', 'identificador':t[1]}]
    t[0] = Concat(t[1], parametro, instrucciones, t.lineno(1), find_column(input, t.slice[1]))


import ply.yacc as yacc
parser = yacc.yacc()
input = ''

def getErrores():
    return errores 

def agregarNativas(ast):
    instrucciones = []

    nombre = "typeof"
    parametro = [{'tipo':'any', 'identificador':'typeof##Param1'}]
    typeof = Typeof(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(typeof)

    nombre = "length"
    parametro = [{'tipo':'any', 'identificador':'length##Param1'}]
    length = Length(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(length)

def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)

#Se va para la interfaz
#file = open("./entrada.txt", "r", encoding="utf-8-sig")
#entrada = file.read()

entrada = '''
interface Actor {
    nombre: string;
    edad: number;
}

interface Pelicula {
    nombre: string;
    posicion: number;
}

interface Contrato {
    actor: Actor;
    pelicula: Pelicula;
}

actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor: Actor, pelicula: Pelicula){
    return {
        actor,
        pelicula
    };
};

function crearActor(nombre: string, edad: number){
    return {
        nombre,
        edad
};
};

function crearPelicula(nombre: string, posicion: number){
    return {
        nombre,
        posicion
    };
};
function imprimir(contrato: Contrato){
    console.log("Actor:", contrato.actor.nombre, "   Edad:", contrato.actor.edad);
    console.log("Pelicula:", contrato.pelicula.nombre, "   Genero:", contrato.pelicula.posicion);
};
function contratos(){
    for (let i = 2; i < 4; i++) {
        let contrato: Contrato = {
        actor: { nombre: "", edad: 0 },
        pelicula: { nombre: "", posicion: 0 }
        };
        if (i < 5) {
        actor = crearActor(actores[i - 1], i + 38);
        pelicula = crearPelicula(peliculas[i - 1], i-1);
        contrato = contratar(actor, pelicula);
        };
        imprimir(contrato);
    };
};

contratos();
'''

instrucciones = parse(entrada) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos('global')
ast.setTSGlobal(TSGlobal)
agregarNativas(ast)

for error in errores: #Captura de errores lexicos y sintacticos 
    ast.getExcepciones().append(error)
    ast.updateConsolaln(error.toString())

for instruccion in ast.getInstrucciones():
    if isinstance(instruccion, Funcion):
        ast.addFuncion(instruccion)
    elif isinstance(instruccion, Struct):
        ast.addStruct(instruccion)
    else:
        valor = instruccion.interpretar(ast,TSGlobal)
        if isinstance(valor, Excepcion):
            ast.getExcepciones().append(valor)
            ast.updateConsolaln(valor.toString())

print(ast.getConsola())
print("salida")


