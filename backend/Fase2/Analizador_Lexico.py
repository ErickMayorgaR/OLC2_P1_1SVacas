import re
import ply.lex as lex

errores = []

#  Entrada: IdentificardorToken
reserved = {
    'console'     :   'RCONSOLE',
    'log'         :   'RLOG',
    'let'         :   'RLET',
    'Any'         :   'ANY',
    'null'        :   'NULL',
    'number'      :   'NUMBER',
    'string'      :   'STRING',
    'boolean'     :   'BOOLEAN',
    'true'        :   'RTRUE',
    'false'       :   'RFALSE',
    'if'          :   'RIF',
    'else'        :   'RELSE',
    'elseif'      :   'RELSEIF',
    'while'       :   'WHILE',
    'for'         :   'FOR',
    'of'          :   'OF',
    'return'      :   'RETURN',
    'break'       :   'BREAK',
    'continue'    :   'CONTINUE',
    'function'    :   'FUNCTION',
}

tokens  = [
    'PUNTO',
    'DPUNTOS',
    'PTCOMA',
    'COMA',
    'PARI',
    'PARD',
    'LLAVEIZQ',
    'LLAVEDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POTENCIA',
    'PORCENTAJE',
    'MENOR',
    'MAYOR',
    'IGUAL',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'OR',
    'AND',
    'NOT',
    'NUMBER',
    'DECIMAL',
    'CADENA',
    'ID',
]+ list(reserved.values())
# Tokens
t_PUNTO         = r'\.'
t_DPUNTOS       = r'\:'
t_PTCOMA        = r'\;'
t_COMA          = r'\,'
t_PARI          = r'\('
t_PARD          = r'\)'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'
t_MAS           = r'\+'
t_MENOS         = r'\-'
t_POR           = r'\*'
t_DIV           = r'\/'
t_POTENCIA      = r'\^'
t_PORCENTAJE    = r'\%'
t_MENOR         = r'\<'
t_MAYOR         = r'\>'
t_IGUAL         = r'\='
t_MAYORIGUAL    = r'\>\='
t_MENORIGUAL    = r'\<\='
t_IGUALIGUAL    = r'\=\='
t_DIFERENTE     = r'\!\='
t_OR            = r'\|\|'
t_AND           = r'\&\&'
t_NOT           = r'\!'

#Decimal
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

#Entero
def t_NUMBER(n):
    r'\d+'
    try:
        if(n.value != None):
            n.value = int(n.value)
        else:
            n.value = 'nothing'
    except ValueError:
        print("Valor del entero demasiado grande %d", n.value)
        n.value = 0
    return n

#Cadena
def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] #Se remueven las comillas de la entrada
    t.value = t.value.replace('\\t','\t')
    t.value = t.value.replace('\\n','\n')
    t.value = t.value.replace('\\"','\"')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\\\','\\')
    return t

#Identificador
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')# Check for reserved words
    return t

#Comentario de Una Linea
def t_Com_Simple(t):
    r'\/\/.*'
    t.lexer.lineno += 1

#Comentario Multilinea
def t_Com_Multiple(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')
    
#Nueva Linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados
t_ignore = " \t"

#Error
def t_error(t):
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex(reflags = re.IGNORECASE)