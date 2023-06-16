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
from src.Instrucciones.Funcion.LlamadaFuncion import LlamadaFuncionStruct
from src.Instrucciones.Sentencias.Return import Return
from src.Instrucciones.Sentencias.Continue import Continue
from src.Instrucciones.Sentencias.Break import Break
from src.Nativas.Fixed import Fixed
from src.Nativas.Exponential import Exponential
from src.Nativas.String import String
from src.Nativas.Lower import Lower
from src.Nativas.Upper import Upper
from src.Nativas.Split import Split
from src.Nativas.Concat import Concat
from src.Nativas.Typeof import Typeof
from src.TS.Tipo import Tipo, OperadorAritmetico, OperadorLogico, OperadorRelacional
from src.TS.Excepcion import Excepcion
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
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

# ///////////////////////////////////////////////////// INSTRUCCIONES A EVALUAR
def p_instrucciones_evaluar(t):
    '''instruccion : imprimir PTCOMA
                    | declaracion_normal PTCOMA
                    | asignacion_normal PTCOMA
                    | condicional_if PTCOMA
                    | funcion PTCOMA
                    | llamada_funcion PTCOMA
                    | inst_return PTCOMA
                    | inst_break PTCOMA
                    | inst_continue PTCOMA'''
    t[0] = t[1]

def p_error(t):
    'instruccion : error PTCOMA'
    errores.append(Excepcion("Sintáctico", "Error sintáctico, " + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = "" 

#///////////////////////////////////////////////////////////FUNCIONES
def p_funcion(t):
    '''funcion : RFUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER
                | RFUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDER'''
    if len(t) == 6:
        t[0] = Funcion(t[2],None,t[6], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////LLAMADA FUNCION
def p_llamada_funcion(t):
    '''llamada_funcion : ID PARI PARD
                        | ID PARI parametros_ll PARD''' 
    # (let nombre: string, let apellido: string, let edad: number)
    if len(t) == 3:
        t[0] = LlamadaFuncionStruct(t[1],None,t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = LlamadaFuncionStruct(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

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
        t[0] = {'tipo': 'any', 'id': t[1]}
    elif len(t) == 4:
        t[0] = {'tipo': t[3], 'id': t[1]}
    else:
        t[0] = {'tipo': t[4], 'id': t[2]}

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
    'imprimir : RCONSOLE PUNTO RLOG PARI expresiones_coma PARD'
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))

# ///////////////////////////////////////////////////// DECLARACION VARIABLES
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    t[0] = DeclaracionVar(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo(t):
    'declaracion_normal : RLET ID IGUAL expresion'
    t[0] = DeclaracionVar(t[2], 'any', t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo_sin_valor(t):
    'declaracion_normal : RLET ID'
    t[0] = DeclaracionVar(t[2], 'any', None, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_valor(t):
    'declaracion_normal : RLET ID DPUNTOS tipo'
    if t[4] == "number":
        t[0] = DeclaracionVar(t[2], t[4], "0", t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "string":
        t[0] = DeclaracionVar(t[2], t[4], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "boolean":
        t[0] = DeclaracionVar(t[2], t[4], "true", t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////ASIGNACION DE VARIABLES
def p_asignacion_var_tipo(t):
    'asignacion_normal : ID IGUAL expresion DPUNTOS DPUNTOS tipo'
    t[0] = AsignacionVar(t[1], t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_var(t):
    'asignacion_normal : ID IGUAL expresion'
    if isinstance(t[3], list):
        t[0] = AsignacionArreglos(t[1], t[3], Tipo.ARREGLO, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = AsignacionVar(t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))    

#///////////////////////////////////////////////////////////SENTENCIAS DE TRANSFERENCIA
def p_return_expresion(t):
    'inst_return : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

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
'''def p_ciclo_While(t):
    'ciclo_while : WHILE PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))
'''

# ///////////////////////////////////////////////////// TIPOS
def p_tipo(t):
    '''tipo : STRING
            | NUMBER
            | BOOLEAN'''
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
    elif p[2] == '^':
        p[0] = Aritmetica(OperadorAritmetico.POTENCIA, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '%':
        p[0] = Aritmetica(OperadorAritmetico.PORCENTAJE, p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))

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
        
        
def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivos(Tipo.NUMBER, int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos(Tipo.NUMBER, float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivos(Tipo.CADENA, str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivos(Tipo.BANDERA, True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos(Tipo.BANDERA, False, t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_identificador(t):
    'expresion : ID'
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////////////////////EXPRESIONES COMA
def p_expresiones_coma_expresiones_coma_expresion(p):
    'expresiones_coma : expresiones_coma COMA expresion'
    p[1].append(p[3])
    p[0] = p[1]

def p_expresiones_coma_expresion(p):
    'expresiones_coma : expresion'
    p[0] = [p[1]]

def agregarNativas(ast):
    instrucciones = []

    nombre = "typeof"
    parametro = [{'tipo':'any', 'id':'typeof##Param1'}]
    typeof = Typeof(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(typeof)

    nombre = "toUpperCase"
    parametro = [{'tipo':'any', 'id':'toUpperCase##Param1'}]
    toUpperCase = Upper(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(toUpperCase)

    nombre = "toLowerCase"
    parametro = [{'tipo':'any', 'id':'toLower##Param1'}]
    toLowerCase = Lower(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(toLowerCase)

    nombre = "toString"
    parametro = [{'tipo':'any', 'id':'toString##Param1'}]
    toString = String(nombre, parametro, instrucciones, -1,-1)
    ast.addFuncion(toString)

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

entrada = '''
let val1:number = 1;
let val2:number = 10;
let val3:number = 2021.2020;
console.log("Probando declaracion de variables \n");
console.log(val1, " ", val2, " ", val3);
console.log("---------------------------------");
// COMENTARIO DE UNA LINEA
let a: number = 5;
console.log(typeof(toString(a))); // llamada a una funcion
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
    valor = instruccion.interpretar(ast, TSGlobal)
    if isinstance(valor, Excepcion):
        ast.getExcepciones().append(valor)
        ast.updateConsolaln(valor.toString())

print(ast.getConsola())
print("salida")


