import ply.yacc as yacc
from src.TS.Tipo import Tipo, OperadorAritmetico, OperadorLogico, OperadorRelacional
from src.Instrucciones.Funcion.LlamadaFuncion import LlamadaFuncionStruct
from src.Instrucciones.Arreglos.Modificacion import ModificacionArreglo
from src.Instrucciones.Arreglos.Asignacion import AsignacionArreglos
from src.Instrucciones.Arreglos.Declaracion import DeclaracionArreglos
from src.Instrucciones.Variables.Declaracion import DeclaracionVar
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Instrucciones.Variables.Asignacion import AsignacionVar
from src.Instrucciones.Sentencias.Continue  import Continue
from src.Instrucciones.Arreglos.Acceso import AccesoArreglo
from src.Expresiones.Identificador import Identificador
from src.Instrucciones.Sentencias.Return  import Return
from src.Instrucciones.Sentencias.Break  import Break
from src.Instrucciones.Funcion.Funcion import Funcion
from src.Expresiones.aritmetica import Aritmetica
from src.Expresiones.relacional import Relacional
from src.Expresiones.primitivos import Primitivos
from src.Instrucciones.imprimir import Imprimir
from src.Expresiones.logica import Logica
from src.TS.Excepcion import Excepcion
from src.Instrucciones.Structs.Struct import Struct
from src.Instrucciones.Structs.Acceso import AccesoStruct
from src.Instrucciones.Structs.Modificacion import ModificacionStruct
from src.Nativas.String import String
from copy import copy

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
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

''' 
                    | modificar_arreglo PTCOMA
                    | funciones_instr PTCOMA
                    | llamada_funcion_instr PTCOMA
                    | break_instr PTCOMA
                    | continue_instr PTCOMA
                    | return_instr PTCOMA
                    | structs_instr PTCOMA
                    | llamada_funcion_struct_instr PTCOMA
                    | modificacion_struct PTCOMA

                    '''
# ///////////////////////////////////////////////////// INSTRUCCIONES A EVALUAR
def p_instrucciones_evaluar(t):
    '''instruccion : imprimir PTCOMA
                    | asignacion_instr PTCOMA
                    | declaracion_var_instr PTCOMA
                    | condicional_if PTCOMA'''
    t[0] = t[1]
    
    
def p_instruccion_error(p):
    'instruccion : error fininstr'
    errores.append(Excepcion("Sintáctico", "Error sintáctico, " + str(p[1].value), p.lineno(1), find_column(input, p.slice[1])))
    p[0] = ""
    
# ///////////////////////////////////////////////////// IMPRIMIR
def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARENTESISA expresion PARENTESISC'
    t[0] = Imprimir(t[5], True, t.lineno(1), find_column(input, t.slice[1]))


# ///////////////////////////////////////////////////// IF CONDICIONAL
def p_condicional_if(t):
    'condicional_if : RIF PARENTESISA expresion PARENTESISC LLAVEA LLAVEC'
    print('Expresion:',t[3])
    t[0] = t[3]


# ///////////////////////////////////////////////////// TIPOS
def p_tipo(t):
    '''tipo : STRING
            | NUMBER
            | BOOLEAN'''
    t[0] = t[1]

# def p_tipo_datos(t):
#     '''tipo : NUMBER
#             | STRING
#             | BOOLEAN'''
#     if t[1].lower() == 'number':
#         t[0] = Tipo.NUMBER
#     elif t[1].lower() == 'string':
#         t[0] = Tipo.CADENA
#     elif t[1].lower() == 'boolean':
#         t[0] = Tipo.BANDERA


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

def p_expresion_binaria_relacional(p):
    '''expresion : expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion'''
    
    if p[2] == '==':
        p[0] = Relacional(OperadorRelacional.IGUALIGUAL, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '!=':
        p[0] = Relacional(OperadorRelacional.DIFERENTE, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '<':
        p[0] = Relacional(OperadorRelacional.MENOR, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '>':
        p[0] = Relacional(OperadorRelacional.MAYOR, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '<=':
        p[0] = Relacional(OperadorRelacional.MENORIGUAL, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '>=':
        p[0] = Relacional(OperadorRelacional.MAYORIGUAL, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))

def p_expresion_binaria_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    if p[2] == '&&':
        p[0] = Logica(OperadorLogico.AND, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '||':
        p[0] = Logica(OperadorLogico.OR, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))

def p_expresion_unaria(p):
    '''expresion : NOT expresion %prec UNOT
                 | MENOS expresion %prec UMINUS'''

    if p[1] == '!':
        p[0] = Logica(OperadorLogico.NOT, p[2], None, p.lineno(1), find_column(input, p.slice[1]))
    elif p[1] == '-':
        p[0] = Aritmetica(OperadorAritmetico.UMENOS, p[2], None, p.lineno(1), find_column(input, p.slice[1]))
        
        
        
#/////////////////////////////////////////////////////////////////////PRIMITIVOS

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivos(Tipo.NUMBER, int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos(Tipo.NUMBER, float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivos(Tipo.CADENA, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivos(Tipo.BANDERA, True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos(Tipo.BANDERA, False, t.lineno(1), find_column(input, t.slice[1]))
        
# def p_expresion_nothing(p):
#     'expresion : NULL'
#     p[0] = Primitivos(Tipo.NULO, p[1], p.lineno(1), find_column(input, p.slice[1]))

# def p_expresion_parentesis(p):
#     'expresion : PARENTESISA expresion PARENTESISC'
#     p[0] = p[2]

# #///////////////////////////////////////////////////////////ASIGNACION DE VARIABLES
# def p_asignacion_var_tipo(p):
#     'asignacion_instr : ID IGUAL expresion DPUNTOS DPUNTOS tipo'
#     p[0] = AsignacionVar(p[1], p[3], p[6], p.lineno(1), find_column(input, p.slice[1]))

# def p_asignacion_var(p):
#     'asignacion_instr : ID IGUAL expresion'
#     if isinstance(p[3], list):
#         p[0] = AsignacionArreglos(p[1], p[3], Tipo.ARREGLO, p.lineno(1), find_column(input, p.slice[1]))
#     else:
#         p[0] = AsignacionVar(p[1], p[3], None, p.lineno(1), find_column(input, p.slice[1]))    
        
        
# #///////////////////////////////////////////////////////////MODIFICAR ARREGLO
# def p_modificar_arreglo(p):
#     'modificar_arreglo : ID lista_dimensiones IGUAL expresion'
#     p[0] = ModificacionArreglo(p[1], p[2], p[4], p.lineno(1), find_column(input, p.slice[1]))


# #///////////////////////////////////////////////////////////ACCESO ARREGLO
# def p_acceso_arreglo(p):
#     'acceso_arreglo : ID lista_dimensiones'
#     p[0] = AccesoArreglo(p[1], p[2], p.lineno(1), find_column(input, p.slice[1]))
 
# def p_lista_dimensiones(p):
#     'lista_dimensiones : lista_dimensiones CORCHETEA expresion CORCHETEC' 
#     p[1].append(p[3])
#     p[0] = p[1]

# def p_lista_dimensione(p):
#     'lista_dimensiones : CORCHETEA expresion CORCHETEC'
#     p[0] = [p[2]] 
        
        
# #///////////////////////////////////////////////////////////DECLARACION DE VARIABLES LOCALES Y GLOBALES
# def p_declaracion_local(p):
#     'declaracion_var_instr : LOCAL ID'
#     p[0] = DeclaracionVar(p[2], None, None, True, False, p.lineno(1), find_column(input, p.slice[1]))

# def p_declaracion_global(p):
#     'declaracion_var_instr : GLOBAL ID'
#     p[0] = DeclaracionVar(p[2], None, None, False, True, p.lineno(1), find_column(input, p.slice[1]))

# def p_declaracion(p):
#     'declaracion_var_instr : ID'
#     p[0] = DeclaracionVar(p[1], None, None, True, False, p.lineno(1), find_column(input, p.slice[1]))
    
    
# #///////////////////////////////////////////////////////////DECLARACION Y ASIGNACION DE VARIABLES LOCALES Y GLOBALES
# def p_declaracion_global_asignacion_var_tipo(p):
#     'declaracion_var_instr : GLOBAL ID IGUAL expresion DPUNTOS DPUNTOS tipo'
#     p[0] = DeclaracionVar(p[2], p[4], p[7], False, True, p.lineno(1), find_column(input, p.slice[1]))    

# def p_declaracion_local_asignacion_var_tipo(p):
#     'declaracion_var_instr : LOCAL ID IGUAL expresion DPUNTOS DPUNTOS tipo'
#     p[0] = DeclaracionVar(p[2], p[4], p[7], True, False, p.lineno(1), find_column(input, p.slice[1]))    

# def p_declaracion_global_asignacion_var(p):
#     'declaracion_var_instr : GLOBAL ID IGUAL expresion'
#     p[0] = DeclaracionVar(p[2], p[4], None, False, True, p.lineno(1), find_column(input, p.slice[1]))    

# def p_declaracion_local_asignacion_var(p):
#     'declaracion_var_instr : LOCAL ID IGUAL expresion'
#     p[0] = DeclaracionVar(p[2], p[4], None, True, False, p.lineno(1), find_column(input, p.slice[1]))    



#///////////////////////////////////////////////////////////IMPRIMIR
# def p_imprimir_vacio(p):
#     'imprimir_instr : RCONSOLE PUNTO RLOG PARENTESISA PARENTESISC'
#     p[0] = Imprimir(None, False, p.lineno(1), find_column(input, p.slice[1]))

# def p_imprimirln_vacio(p):
#     'imprimir_instr : RCONSOLE PUNTO RLOG PARENTESISA PARENTESISC'
#     p[0] = Imprimir(None, False, p.lineno(1), find_column(input, p.slice[1]))

# def p_imprimir_expresiones_coma(p):
#     'imprimir_instr : RCONSOLE PUNTO RLOG PARENTESISA expresiones_coma PARENTESISC'
#     p[0] = Imprimir(p[5], False, p.lineno(1), find_column(input, p.slice[1]))

# def p_imprimirln_expresiones_coma(p):
#     'imprimir_instr : RCONSOLE PUNTO RLOG PARENTESISA expresiones_coma PARENTESISC'
#     p[0] = Imprimir(p[5], True, p.lineno(1), find_column(input, p.slice[1]))

#///////////////////////////////////////////////////////////FUNCIONES
# def p_funciones(p):
#     'funciones_instr : FUNCTION ID PARENTESISA PARENTESISC instrucciones END'
#     p[0] = Funcion(p[2], [], p[5], p.lineno(1), find_column(input, p.slice[1]))

# def p_funciones_parametros(p):
#     'funciones_instr : FUNCTION ID PARENTESISA parametros PARENTESISC instrucciones END'
#     p[0] = Funcion(p[2], p[4], p[6], p.lineno(1), find_column(input, p.slice[1]))

# #///////////////////////////////////////////////////////////PARAMETROS DE FUNCION
# def p_parametros_funcion(p):
#     'parametros : parametros COMA parametro'
#     p[1].append(p[3])
#     p[0] = p[1] 

# def p_parametros_parametro(p):
#     'parametros : parametro'
#     p[0] = [p[1]]

# #///////////////////////////////////////////////////////////PARAMETRO DE FUNCION
# def p_parametro_tipo(p):
#     'parametro : ID DPUNTOS DPUNTOS tipo'
#     p[0] = {'tipo' : p[4],'identificador' : p[1]}

# def p_parametro(p):
#     'parametro : ID'
#     p[0] = {'tipo' : None,'identificador' : p[1]}

# #///////////////////////////////////////////////////////////LLAMADA FUNCION
# def p_llamada_funcion(p):
#     'llamada_funcion_instr : ID PARENTESISA PARENTESISC'
#     p[0] = LlamadaFuncionStruct(p[1], [], p.lineno(1), find_column(input, p.slice[1]))

# #///////////////////////////////////////////////////////////LLAMADA FUNCION / LLAMADA STRUCT
# def p_llamada_funcion_parametros(p):
#     'llamada_funcion_struct_instr : ID PARENTESISA parametros_llamada PARENTESISC'
#     p[0] = LlamadaFuncionStruct(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))
    
# #///////////////////////////////////////////////////////////PARAMETOS LLAMADA FUNCION
# def p_parametros_llamada_funcion(p):
#     'parametros_llamada : parametros_llamada COMA expresion '
#     p[1].append(p[3])
#     p[0] = p[1]

# def p_parametros_llamada_expresion(p):
#     'parametros_llamada : expresion'
#     p[0] = [p[1]]


# #///////////////////////////////////////////////////////////SENTENCIAS DE TRANSFERENCIA
# def p_sentencia_transferencia_return_expresion(p):
#     'return_instr : RETURN expresion'
#     p[0] = Return(p[2], p.lineno(1), find_column(input, p.slice[1]))

# def p_sentencia_transferencia_return(p):
#     'return_instr : RETURN'
#     p[0] = Return(None, p.lineno(1), find_column(input, p.slice[1]))

# def p_sentencia_transferencia_break(p):
#     'break_instr : BREAK'
#     p[0] = Break(p.lineno(1), find_column(input, p.slice[1]))

# def p_sentencia_transferencia_continue(p):
#     'continue_instr : CONTINUE'
#     p[0] = Continue(p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_identificador(p):
    'expresion : ID'
    p[0] = Identificador(p[1], p.lineno(1), find_column(input, p.slice[1]))

# def p_expresion_llamada_funcion(p):
#     'expresion : llamada_funcion_instr'
#     p[0] = p[1]

# def p_expresion_llamada_funcion_struct(p):
#     'expresion : llamada_funcion_struct_instr'
#     p[0] = p[1]

# def p_lista_expresiones(p):
#     'expresion : CORCHETEA expresiones_coma CORCHETEC'
#     p[0] = p[2]

# def p_acceso_arreglo_expresion(p):
#     'expresion : acceso_arreglo'
#     p[0] = p[1]

# def p_acceso_struct_expresion(p):
#     'expresion : acceso_struct'
#     p[0] = p[1]
    
       
    
# #///////////////////////////////////////////////////////////EXPRESIONES COMA
# def p_expresiones_coma_expresiones_coma_epxresion(p):
#     'expresiones_coma : expresiones_coma COMA expresion'
#     p[1].append(p[3])
#     p[0] = p[1]

# def p_expresiones_coma_expresion(p):
#     'expresiones_coma : expresion'
#     p[0] = [p[1]]
    

# #///////////////////////////////////////////////////////////STRUCTS
# def p_struct(p):
#     '''structs_instr : structs_inmutable
#                      | structs_mutable'''
#     p[0] = p[1]

# def p_structs_inmutable(p):
#     'structs_inmutable : STRUCT ID lista_atributos END'
#     p[0] = Struct(p[2], p[3], False, p.lineno(1), find_column(input, p.slice[1]))

# def p_structs_mutable(p):
#     'structs_mutable : MUTABLE STRUCT ID lista_atributos END'
#     p[0] = Struct(p[3], p[4], True, p.lineno(1), find_column(input, p.slice[1]))

# #///////////////////////////////////////////////////////////ATRIBUTOS
# def p_atributos_atributos(p):
#     'lista_atributos : lista_atributos atributo fininstr'
#     p[1].append(p[2])
#     p[0] = p[1] 

# def p_atributos(p):
#     'lista_atributos : atributo fininstr'
#     p[0] = [p[1]]

# #///////////////////////////////////////////////////////////ATRIBUTO
# def p_atributo_tipo(p):
#     'atributo : ID DPUNTOS DPUNTOS tipo'
#     p[0] = {'tipo' : p[4],'identificador' : p[1]}

# def p_atributo(p):
#     'atributo : ID'
#     p[0] = {'tipo' : None,'identificador' : p[1]}

# #///////////////////////////////////////////////////////////ACCESO STRUCT
# def p_acceso_struct(p):
#     'acceso_struct : ID PUNTO ID'
#     p[0] = AccesoStruct(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))

# #///////////////////////////////////////////////////////////MODIFICACION STRUCT
# def p_modificacion_struct(p):
#     'modificacion_struct : ID PUNTO ID IGUAL expresion'
#     p[0] = ModificacionStruct(p[1], p[3], p[5], p.lineno(1), find_column(input, p.slice[1]))


# #//////////////////////////////////////////////NATIVAS EXTRA

# from src.Nativas.Upper import Upper
# from src.Nativas.Lower import Lower


# def crearNativas(ast): #Creacion y declaracion de funciones nativas
#     identificador = 'lowercase'
#     parametros = [{'tipo': Tipo.CADENA, 'dimensiones': None, 'identificador': 'Lower$$Parametros123'}]
#     instrucciones = []
#     lowercase = Lower(identificador, parametros, instrucciones, -1, -1)
#     ast.addFuncion(lowercase)

    
#     identificador = 'uppercase'
#     parametros = [{'tipo': Tipo.CADENA, 'dimensiones': [], 'identificador': 'Upper$$Parametros123'}]
#     instrucciones = []
#     uppercase = Upper(identificador, parametros, instrucciones, -1, -1)
#     ast.addFuncion(uppercase)


# def p_parse_string(p):
#     'expresion : STRING PARENTESISA expresion PARENTESISC'
#     p[0] = String(p[3], p.lineno(1), find_column(input, p.slice[1]))

def getErrores():
    return errores 

input = ''

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

from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos

entrada = '''
console.log(4<5&&9>7); // No la camioneta vaconsole.log(4+2-6*3);
'''

instrucciones = parse(entrada) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos('global')
ast.setTSGlobal(TSGlobal)

for error in errores: #Captura de errores lexicos y sintacticos 
    ast.getExcepciones().append(error)
    ast.updateConsolaln(error.toString())

for instruccion in ast.getInstrucciones():
    valor = instruccion.interpretar(ast, TSGlobal)
    if isinstance(valor, Excepcion):
        ast.getExcepciones().append(valor)
        ast.updateConsolaln(valor.toString())

print(ast.getConsola())


