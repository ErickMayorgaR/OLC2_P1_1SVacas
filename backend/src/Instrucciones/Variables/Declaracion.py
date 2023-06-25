from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Tipo import Tipo

class DeclaracionVar(Instruccion):
    def __init__(self, identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.valor = valor
        self.tipo = tipo
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        simboloVar = table.getTabla(str(self.identificador))
        if simboloVar != None:
            tablaSimboloVar = table.getRealTabla(str(self.identificador))
            #faltan errores semanticos


        if self.valor != None: #Si viene un valor
            value = self.valor.interpretar(tree, table)
            if isinstance(value, Excepcion):
                return value
               
            if self.tipo == 'any': #Verifica si el tipo de la var no viene
                self.tipo = self.valor.tipo #Le asigna el tipo a la var
            if self.tipo != self.valor.tipo: #Verifica que las variables sean del mismo tipo 
                return Excepcion("Semántico", "El tipo de dato en la variable \""+self.identificador+"\" es diferente", self.fila, self.columna) 
            
            simbolo = Simbolo(str(self.identificador), self.tipo, value, self.fila, self.columna)
        elif self.valor == None :
            simbolo = Simbolo(str(self.identificador), Tipo.NULO, None, self.fila, self.columna)
                
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion):
            return result
        return None
        
        
    def getNode(self):
        nodo = NodeCst("declaracion_var_instr")
        nodo.addChild(str(self.identificador))

        if self.tipo != None:
            nodo.addChild(str(self.tipoDato(self.tipo)))

        if self.valor != None:
            nodo.addChildNode(self.valor.getNode())
        return nodo

    def tipoDato(self, tipo):
        if tipo == Tipo.BANDERA:
            return "bool"
        elif tipo == Tipo.CADENA:
            return "string"
        elif tipo == Tipo.CARACTER:
            return "char"
        elif tipo == Tipo.NUMBER:
            return "number"
        elif tipo == Tipo.NULO:
            return "Nothing"