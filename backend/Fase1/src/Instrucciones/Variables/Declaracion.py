from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo

class DeclaracionVar(Instruccion):
    def __init__(self, identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.valor = valor
        self.tipo = tipo
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        simboloVar = table.getTabla(str(self.identificador))
        if simboloVar != None:
            return Excepcion("Semántico", "La variable \""+self.identificador+"\" ya esta declarada.", self.fila, self.columna) 
            #faltan errores semanticos

        if self.valor != None: #Si viene un valor
            if self.tipo == 'array':
                resultados = []
                for element in self.valor:
                    value = element.interpretar(tree, table)
                    if isinstance(value, Excepcion):
                        return value
                    resultados.append(value)

                simbolo = Simbolo(str(self.identificador), self.tipo, resultados, self.fila, self.columna)
            else:
                value = self.valor.interpretar(tree, table)
                if isinstance(value, Excepcion):
                    return value
                
                if self.tipo == 'any': #Verifica si el tipo de la var no viene
                    self.tipo = self.valor.tipo #Le asigna el tipo a la var
                if self.tipo != self.valor.tipo: #Verifica que las variables sean del mismo tipo 
                    return Excepcion("Semántico", "El tipo de dato en la variable \""+self.identificador+"\" es diferente", self.fila, self.columna) 
                
                simbolo = Simbolo(str(self.identificador), self.tipo, value, self.fila, self.columna)
        
        elif self.valor == None :
            simbolo = Simbolo(str(self.identificador), 'any', None, self.fila, self.columna)
                
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
        if tipo ==  'boolean':
            return "Bool"
        elif tipo == 'string':
            return "String"
        elif tipo == 'number':
            return "Number"
        elif tipo == 'any':
            return "Anything"