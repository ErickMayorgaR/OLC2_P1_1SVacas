import ply.yacc as yacc
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Expresiones.Aritmeticas.Division import Division
from src.Expresiones.Aritmeticas.Modulo import Modulo
from src.Expresiones.Aritmeticas.Multiplicacion import Multiplicacion
from src.Expresiones.Aritmeticas.Potencia import Potencia
from src.Expresiones.Aritmeticas.Resta import Resta
from src.Expresiones.Aritmeticas.Suma import Suma
from src.Expresiones.Logicas.And import And
from src.Expresiones.Logicas.Not import Not
from src.Expresiones.Logicas.Or import Or
from src.Expresiones.Primitivos.Boolean import Boolean
from src.Expresiones.Primitivos.Identificador import Identificador
from src.Expresiones.Primitivos.Negativo import Negativo
from src.Expresiones.Primitivos.Null import Null 
from src.Expresiones.Primitivos.Number import Number
from src.Expresiones.Primitivos.String import String
from src.Instrucciones.Funcion.Funcion import Funcion
from src.Instrucciones.Funcion.LlamadaFuncion import LlamadaFuncion
from src.Expresiones.Primitivos.Temp import Temporal
from src.Expresiones.Relaciones.Diferente import Diferente
from src.Expresiones.Relaciones.IgualIgual import IgualIgual
from src.Expresiones.Relaciones.Mayor import Mayor
from src.Expresiones.Relaciones.MayorIgual import MayorIgual
from src.Expresiones.Relaciones.Menor import Menor
from src.Expresiones.Relaciones.MenorIgual import MenorIgual
from src.Instrucciones.imprimir import Imprimir
from src.Instrucciones.Sentencias.If import If
from src.Instrucciones.Sentencias.While import While
from src.Instrucciones.Sentencias.For import For
from src.Instrucciones.Sentencias.Return import Return
from src.Instrucciones.Sentencias.Continue import Continue
from src.Instrucciones.Sentencias.Break import Break
from src.Instrucciones.Variables.Declaracion import DeclaracionVar
from src.Instrucciones.Variables.Asignacion import AsignacionVar
from src.TS.Tipo import Tipo, OperadorAritmetico, OperadorLogico, OperadorRelacional
from src.TS.Excepcion import Excepcion
from src.TS.TablaSimbolos import TablaSimbolos
from src.C3DGen.generador import Generador
from src.TS.Arbol import Arbol
from src.Nativas.Diferente import StringDiferente
from src.Nativas.Concatenar import ConcatenacionString
from src.Nativas.Elevar import ElevarString
from src.Nativas.Igual import StringIgual
from src.Nativas.Mayor import StringMayor
from src.Nativas.MayorIgual import StringMayorIgual
from src.Nativas.Menor import StringMenor
from src.Nativas.MenorIgual import StringMenorIgual
from src.Nativas.Potencia import FuncPotencia
from src.Nativas.PrintString import PrintString
from copy import copy

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL', ),
    ('left','MAS','MENOS'),
    ('left', 'POR', 'DIV', 'PORCENTAJE'),
    ('left','PARI', 'PARD'),
    ('nonassoc', 'POTENCIA'), 
    ('right','UMINUS'),
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
                   | asignacion_instr PTCOMA
                   | if_instr
                   | for_instr 
                   | while_instr 
                   | return_instr PTCOMA
                   | continue_instr PTCOMA
                   | break_instr PTCOMA
                   | llamada_funcion_instr PTCOMA
                   | funciones_instr
                   | llamada_funcion_struct_instr PTCOMA 
                    '''
    t[0] = t[1]
    
    
def p_error(t):
    'instruccion : error PTCOMA'
    errores.append(Excepcion("Sintáctico", "Error sintáctico, " + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = "" 

# ///////////////////////////////////////////////////// IMPRIMIR
def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARI expresiones_coma PARD'
    t[0] = Imprimir(t[5], True, t.lineno(1), find_column(input, t.slice[1]))



# ///////////////////////////////////////////////////// DECLARACION VARIABLES
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    t[0] = DeclaracionVar(t[2], t[6], t[4], False, True, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo(t):
    'declaracion_normal : RLET ID IGUAL expresion'
    t[0] = DeclaracionVar(t[2], t[4], None, False, True, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_tipo_sin_valor(t):
    'declaracion_normal : RLET ID'
    t[0] = DeclaracionVar(t[2], None, None, False, True, t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_sin_valor(t):
    'declaracion_normal : RLET ID DPUNTOS tipo'
    if t[4] == "number":
        t[0] = DeclaracionVar(t[2], "0", Tipo.NUMBER, False, True, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "string":
        t[0] = DeclaracionVar(t[2], "", Tipo.CADENA, False, True, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == "boolean":
        t[0] = DeclaracionVar(t[2], "true", Tipo.BANDERA, False, True, t.lineno(1), find_column(input, t.slice[1]))
		
  
  
#///////////////////////////////////////////////////////////ASIGNACION DE VARIABLES
def p_asignacion_var_tipo(p):
    'asignacion_instr : ID IGUAL expresion DPUNTOS DPUNTOS tipo'
    p[0] = AsignacionVar(p[1], p[3], p[6], p.lineno(1), find_column(input, p.slice[1]))

def p_asignacion_var(p):
    'asignacion_instr : ID IGUAL expresion'
    if isinstance(p[3], list):
        p[0] = ''
    else:
        p[0] = AsignacionVar(p[1], p[3], None, p.lineno(1), find_column(input, p.slice[1])) 
        
        


#///////////////////////////////////////////////////////////WHILE
def p_While(p):
    'while_instr : WHILE PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = While(p[3], p[6], p.lineno(1), find_column(input, p.slice[1]))

#///////////////////////////////////////////////////////////FOR
def p_for_string(p): #Lo hace con strings y arreglos
    'for_instr : FOR PARI RLET ID OF expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = For(p[4], p[6], None, p[9], None, p.lineno(1), find_column(input, p.slice[1]))

def p_for_rango(p): #Lo hace con rango
    'for_instr : FOR PARI RLET ID IGUAL expresion PTCOMA expresion PTCOMA ID MAS MAS PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = For(p[4], p[6], p[8], p[15], p[10], p.lineno(1), find_column(input, p.slice[1]))
    
    

#///////////////////////////////////////////////////////////SENTENCIAS DE TRANSFERENCIA
def p_sentencia_transferencia_return_expresion(p):
    'return_instr : RETURN expresion'
    p[0] = Return(p[2], p.lineno(1), find_column(input, p.slice[1]))

def p_sentencia_transferencia_return(p):
    'return_instr : RETURN'
    p[0] = Return(None, p.lineno(1), find_column(input, p.slice[1]))

def p_sentencia_transferencia_break(p):
    'break_instr : BREAK'
    p[0] = Break(p.lineno(1), find_column(input, p.slice[1]))

def p_sentencia_transferencia_continue(p):
    'continue_instr : CONTINUE'
    p[0] = Continue(p.lineno(1), find_column(input, p.slice[1]))

        
        
#///////////////////////////////////////////////////////////FUNCIONES
def p_funciones(p):
    'funciones_instr : FUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = Funcion(p[2], [], Tipo.NULO, p[6], p.lineno(1), find_column(input, p.slice[1]))

def p_funciones_parametros(p):
    'funciones_instr : FUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = Funcion(p[2], p[4], Tipo.NULO, p[7], p.lineno(1), find_column(input, p.slice[1]))



#///////////////////////////////////////////////////////////PARAMETROS DE FUNCION
def p_parametros_funcion(p):
    'parametros : parametros COMA parametro'
    p[1].append(p[3])
    p[0] = p[1] 

def p_parametros_parametro(p):
    'parametros : parametro'
    p[0] = [p[1]]

#///////////////////////////////////////////////////////////PARAMETRO DE FUNCION
def p_parametro_tipo(p):
    'parametro : ID DPUNTOS tipo'
    p[0] = {'tipo' : p[3],'identificador' : p[1]}


#///////////////////////////////////////////////////////////LLAMADA FUNCION
def p_llamada_funcion(p):
    'llamada_funcion_instr : ID PARI PARD'
    p[0] = LlamadaFuncion(p[1], [], p.lineno(1), find_column(input, p.slice[1]))

#///////////////////////////////////////////////////////////LLAMADA FUNCION / LLAMADA STRUCT
def p_llamada_funcion_parametros(p):
    'llamada_funcion_struct_instr : ID PARI parametros_llamada PARD'
    p[0] = LlamadaFuncion(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))
    
#///////////////////////////////////////////////////////////PARAMETOS LLAMADA FUNCION
def p_parametros_llamada_funcion(p):
    'parametros_llamada : parametros_llamada COMA expresion '
    p[1].append(p[3])
    p[0] = p[1]

def p_parametros_llamada_expresion(p):
    'parametros_llamada : expresion'
    p[0] = [p[1]]

        

#///////////////////////////////////////////////////////////SENTENCIAS DE CONTROL
def p_if(p):
    'if_instr : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = If(p[3], p[6], None, None, p.lineno(1), find_column(input, p.slice[1]))

def p_if_elseif_else(p):
    'if_instr : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER elseifs_instr RELSE LLAVEIZQ instrucciones LLAVEDER'
    p[0] = If(p[3], p[6], p[11], p[8], p.lineno(1), find_column(input, p.slice[1]))

def p_if_elseif(p):
    'if_instr : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER elseifs_instr'
    p[0] = If(p[3], p[6], None, p[8], p.lineno(1), find_column(input, p.slice[1]))

def p_if_else(p):
    'if_instr : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE LLAVEIZQ instrucciones LLAVEDER'
    p[0] = If(p[3], p[6], p[10], None, p.lineno(1), find_column(input, p.slice[1]))

def p_elseifs_elseifs_elseif(p):
    'elseifs_instr : elseifs_instr elseif_instr'
    if p[2] != "":
        p[1].append(p[2])
    p[0] = p[1] 

def p_elseifs_elseif(p):
    'elseifs_instr : elseif_instr'
    if p[1] == "":
        p[0] = []
    else:
        p[0] = [p[1]] 

def p_elseif(p):
    'elseif_instr : RELSEIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    p[0] = If(p[3], p[6], None, None, p.lineno(1), find_column(input, p.slice[1]))


#///////////////////////////////////////////////////////////TIPO DE DATOS
def p_tipo_datos(p):
    '''tipo : STRING
            | NUMBER
            | BOOLEAN'''
    if p[1].lower() == 'number':
        p[0] = Tipo.NUMBER
    elif p[1].lower() == 'string':
        p[0] = Tipo.CADENA
    elif p[1].lower() == 'boolean':
        p[0] = Tipo.BANDERA

#///////////////////////////////////////////////////////////EXPRESION
def p_expresion_parentesis(p):
    'expresion : PARI expresion PARD'
    p[0] = p[2]

def p_expresion_string(p):
    'expresion : CADENA'
    p[0] = String(p[1], Tipo.CADENA, p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_integer(p):
    'expresion : NUMBER'
    p[0] = Number(p[1], Tipo.NUMBER, p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_integer_negative(p):
    'expresion : MENOS NUMBER %prec UMINUS'
    p[0] = Negativo(p[2], Tipo.NUMBER, p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_nothing(p):
    'expresion : NULL'
    p[0] = Null('NULL', Tipo.NULO, p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_identificador(p):
    'expresion : ID'
    p[0] = Identificador(p[1], p.lineno(1), find_column(input, p.slice[1]))

#///////////////////////////////////////////////////////////BOOLEAN
def p_expresion_boolean(p):
    '''expresion : RTRUE
               | RFALSE'''
    if p[1].lower() == 'true':
        p[1] = True
    elif p[1].lower() == 'false':
        p[1] == False

    p[0] = Boolean(p[1], Tipo.BANDERA, p.lineno(1), find_column(input, p.slice[1]))

def p_expresion_binaria_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion
                 | expresion POTENCIA expresion
                 | expresion PORCENTAJE expresion'''
    
    if p[2] == '+':
        p[0] = Suma(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '-':
        p[0] = Resta(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '*':
        p[0] = Multiplicacion(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '/':
        p[0] = Division(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '^':
        p[0] = Potencia(p[1], p[3],p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '%':
        p[0] = Modulo(p[1], p[3],p.lineno(2), find_column(input, p.slice[2]))

def p_expresion_binaria_relacional(p):
    '''expresion : expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion'''
    
    if p[2] == '==':
        p[0] = IgualIgual(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '!=':
        p[0] = Diferente(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '<':
        p[0] = Menor(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '>':
        p[0] = Mayor(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '<=':
        p[0] = MenorIgual(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '>=':
        p[0] = MayorIgual(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))

def p_expresion_binaria_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''

    if p[2] == '&&':
        p[0] = And(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))
    elif p[2] == '||':
        p[0] = Or(p[1], p[3], p.lineno(2), find_column(input, p.slice[2]))

def p_expresion_unaria(p):
    'expresion : NOT expresion %prec UNOT'
    p[0] = Not(p[2], p.lineno(1), find_column(input, p.slice[1]))

#///////////////////////////////////////////////////////////EXPRESIONES COMA
def p_expresiones_coma_expresiones_coma_epxresion(p):
    'expresiones_coma : expresiones_coma COMA expresion'
    p[1].append(p[3])
    p[0] = p[1]

def p_expresiones_coma_expresion(p):
    'expresiones_coma : expresion'
    p[0] = [p[1]]


import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores 


def crearNativas(ast): #Creacion y declaracion de funciones nativas
    identificador = 'Print_String_armc'
    parametros = [{'tipo': Tipo.CADENA, 'dimensiones': None, 'identificador': 'Print_String_armc'}]
    instrucciones = []
    printstring = PrintString(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(printstring)

    identificador = 'Potencia_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'Potencia_armc'}]
    instrucciones = []
    potencia = FuncPotencia(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(potencia)

    identificador = 'Concatenar_String_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'Concatenar_String_armc'}]
    instrucciones = []
    concatenacion = ConcatenacionString(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(concatenacion)

    identificador = 'Elevar_String_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'Elevar_String_armc'}]
    instrucciones = []
    elevacion = ElevarString(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(elevacion)

    identificador = 'String_Diferente_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Diferente_armc'}]
    instrucciones = []
    diferente = StringDiferente(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(diferente)

    identificador = 'String_Igual_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Igual_armc'}]
    instrucciones = []
    igual = StringIgual(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(igual)

    identificador = 'String_Mayor_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Mayor_armc'}]
    instrucciones = []
    mayor = StringMayor(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(mayor)

    identificador = 'String_Mayor_Igual_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Mayor_Igual_armc'}]
    instrucciones = []
    mayorIgual = StringMayorIgual(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(mayorIgual)

    identificador = 'String_Menor_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Menor_armc'}]
    instrucciones = []
    menor = StringMenor(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(menor)

    identificador = 'String_Menor_Igual_armc'
    parametros = [{'tipo': Tipo.NUMBER, 'dimensiones': None, 'identificador': 'String_Menor_Igual_armc'}]
    instrucciones = []
    menorIgual = StringMenorIgual(identificador, parametros, instrucciones, -1, -1)
    ast.addFuncion(menorIgual)
    


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
let hola = 5;

function prueba(){
    console.log("entro a la funcion");
    return 5;
}

console.log(hola);
prueba();

'''


instrucciones = parse(entrada) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos('global')
ast.setTSGlobal(TSGlobal)
label = 0
temporal = 0
indices = {'temporal' : 0, 'label' : 0}
generator = Generador(indices)

generatorFunction = Generador(indices)
generatorFunction.funcion = True
crearNativas(ast)

for func in ast.getFunciones():
    valor = func.interpretar(ast, TSGlobal, generatorFunction)
    if isinstance(valor, Excepcion):
        ast.getExcepciones().append(valor)
        ast.setConsola('')
    else:
        generatorFunction.addInstruction(ast.getConsola())
        ast.setConsola('')


for error in errores: #Captura de errores lexicos y sintacticos 
    ast.getExcepciones().append(error)
    ast.updateConsolaln(error.toString())


for instruccion in ast.getInstrucciones():
    if isinstance(instruccion, Funcion):
        ast.addFuncion(instruccion)
        valor = instruccion.interpretar(ast, TSGlobal, generatorFunction)
        generatorFunction.LabelReturn = ''
    else:
        valor = instruccion.interpretar(ast, TSGlobal, generator)
        
    if isinstance(valor, Excepcion):
        ast.getExcepciones().append(valor)
        ast.setConsola('')
    else:
        if isinstance(instruccion, Funcion):
            generatorFunction.addInstruction(ast.getConsola())
            ast.setConsola('')
        else:
            generator.addInstruction(ast.getConsola())
            ast.setConsola('')


file = open("./Salida.txt", "w")
file.write(generator.getCode(generatorFunction))
file.close()

for error in ast.getExcepciones():
    print(error.toString())