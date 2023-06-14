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
from src.Instrucciones.Variables.Declaracion import Declaracion
from src.TS.Tipo import Tipo, OperadorAritmetico, OperadorLogico, OperadorRelacional
from src.TS.Excepcion import Excepcion
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
                    | condicional_if PTCOMA
                    | ciclo_while PTCOMA'''
    t[0] = t[1]

def p_error(t):
    'instruccion : error PTCOMA'
    errores.append(Excepcion("Sintáctico", "Error sintáctico, " + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = "" 


# ///////////////////////////////////////////////////// IMPRIMIR
def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARI expresion PARD'
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))


# ///////////////////////////////////////////////////// DECLARACION VARIABLES
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    t[0] = Declaracion(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo(t):
    'declaracion_normal : RLET ID IGUAL expresion'
    t[0] = Declaracion(t[2], any, t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo_sin_valor(t):
    'declaracion_normal : RLET ID'
    t[0] = Declaracion(t[2], any, None, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_valor(t):
    'declaracion_normal : RLET ID DPUNTOS tipo'
    if t[4] = "number":
        t[0] = Declaracion(t[2], t[4], 0, t.lineno(1), find_column(input, t.slice[1]))

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
def p_ciclo_While(t):
    'ciclo_while : WHILE PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))


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
    t[0] = Primitivos(Tipo.CADENA, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivos(Tipo.BANDERA, True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos(Tipo.BANDERA, False, t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_identificador(p):
    'expresion : ID'
    p[0] = Identificador(p[1], p.lineno(1), find_column(input, p.slice[1]))

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
let var1 = 0;
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
print("salida")


