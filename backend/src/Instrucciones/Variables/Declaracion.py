from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Tipo import Tipo

class DeclaracionVar(Instruccion):
    def __init__(self, identificador, valor, tipo, local, globall, fila, columna):
        self.identificador = identificador
        self.valor = valor
        self.tipo = tipo
        self.local = local
        self.globall = globall
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
    #AUN DEBES VALIDAR SI SOLO DECLARAN LA VARIABLE LOCAL PERO NO LE ASIGNAN VALOR Y LA USAN COMO CONTADOR
        simboloVar = table.getTabla(str(self.identificador))
        if simboloVar != None:
            tablaSimboloVar = table.getRealTabla(str(self.identificador))
            if simboloVar.local == True and self.globall == True:
                return Excepcion("Semántico", "No se puede declarar una variable global donde ya existe una variable local", self.fila, self.columna) 
            elif simboloVar.local == True and self.local == True and tablaSimboloVar == table:
                return Excepcion("Semántico", "No se puede declarar una variable local donde ya existe una variable local", self.fila, self.columna) 


        if self.valor != None: #Si viene un valor
            value = self.valor.interpretar(tree, table)
            if isinstance(value, Excepcion):
                return value
            
            if self.tipo == None: #Verifica si el tipo de la var no viene
                self.tipo = self.valor.tipo #Le asigna el tipo a la var

            if self.tipo != self.valor.tipo: #Verifica que las variables sean del mismo tipo 
                return Excepcion("Semántico", "El tipo de dato en la variable \""+self.identificador+"\" es diferente", self.fila, self.columna) 

        
        if self.local: #Se encarga de las variable locales
            if simboloVar != None:
                if self.valor != None:
                    simbolo = Simbolo(str(self.identificador), self.tipo, value, True, False, self.fila, self.columna)
                elif self.valor == None :
                    simbolo = Simbolo(str(self.identificador), Tipo.NULO, None, True, False, self.fila, self.columna)
            else:
                simbolo = Simbolo(str(self.identificador), Tipo.NULO, None, True, False, self.fila, self.columna)
        
        elif self.globall: #Se encarga de las variables globales
            
            if self.valor != None: #Si la variable trae valor
                simbolo = Simbolo(str(self.identificador), self.tipo, value, False, True, self.fila, self.columna)
                if simboloVar == None: #Verifica si la variable no estaba declarada anteriormente de modo global        
                    return Excepcion("Semántico", "La variable \""+self.identificador+"\" no existe en el entorno global", self.fila, self.columna) 
                elif simboloVar != None:#Verifica si la variable ya estaba declarada anteriormente de modo global
                    resultGlobal = tree.getTSGlobal().actualizarTabla(simbolo) #Actualiza el simbolo al entorno global
                    if isinstance(resultGlobal, Excepcion):
                        return resultGlobal
            
            elif self.valor == None:#Si la variable no trae valor
                if simboloVar == None: #Verifica si la variable no estaba declarada anteriormente de modo global        
                    return Excepcion("Semántico", "La variable \""+self.identificador+"\" no existe en el entorno global", self.fila, self.columna) 
                elif simboloVar != None: #Verifica si la variable ya estaba declarada anteriormente de modo global
                    simbolo = Simbolo(str(self.identificador), simboloVar.tipo, simboloVar.valor, False, True, self.fila, self.columna)

        result = table.setTabla(simbolo)  #pos namas estamos mandando el identificador a la tablita jeje
        if isinstance(result, Excepcion):
            return result

        return None
        
        
    def getNode(self):
        nodo = NodeCst("declaracion_var_instr")
        if self.local:
            nodo.addChild(str('LOCAL'))
        elif self.globall:
            nodo.addChild(str('GLOBAL'))

        nodo.addChild(str(self.identificador))

        if self.tipo != None:
            nodo.addChild(str(self.tipoDato(self.tipo)))

        if self.valor != None:
            nodo.addChildNode(self.valor.getNode())
        return nodo

    def tipoDato(self, tipo):
        if tipo == Tipo.BANDERA:
            return "Bool"
        elif tipo == Tipo.CADENA:
            return "String"
        elif tipo == Tipo.CARACTER:
            return "Char"
        elif tipo == Tipo.DOBLE:
            return "Float64"
        elif tipo == Tipo.NUMBER:
            return "Int64"
        elif tipo == Tipo.NULO:
            return "Nothing"