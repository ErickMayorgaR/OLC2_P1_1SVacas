from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
import src.Instrucciones.globals as globals
from copy import copy
class DeclaracionVar(Instruccion):
    def __init__(self, identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.valor = valor
        self.tipo = tipo
        self.value = ""
        super().__init__(fila, columna)

    def interpretar(self, tree, table):
        var_For = globals.FlagFor
        simboloVar = table.getTabla(str(self.identificador))
        if simboloVar != None and var_For == False:
            return Excepcion("Semántico", "La variable \""+self.identificador+"\" ya esta declarada.", self.fila, self.columna) 
            #faltan errores semanticos

        if simboloVar != None and var_For == True:
            return None

        if self.valor != None: #Si viene un valor
            if self.tipo == 'array':
                value = copy(self.valor)
                self.copiarArreglo(value, self.valor)
                val = self.interpretarArreglos(tree, table, value)
                if isinstance(val, Excepcion):
                    return val
                self.value = value
                simbolo = Simbolo(str(self.identificador), self.tipo, value, self.fila, self.columna)

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
        
    def interpretarArreglos(self, tree, table, arreglo):
        i = 0
        while i < len(arreglo):
            if isinstance(arreglo[i], list):
                self.interpretarArreglos(tree, table, arreglo[i])
            else:
                valor = arreglo[i].interpretar(tree, table)
                if isinstance(valor, Excepcion):
                    return valor
                arreglo[i] = valor
            i += 1
        return None
                  
    def copiarArreglo(self, valor, arreglo):
        i = 0
        while i < len(arreglo):
            if isinstance(arreglo[i], list):
                valor[i] = copy(arreglo[i])
            else:
                valor[i] = copy(arreglo[i])
            i += 1
        return None 
      
    def getNode(self):
        nodo = NodeCst("declaracion_var_instr")
        nodo.addChild(str(self.identificador))

        if self.tipo != None:
            nodo.addChild(str(self.tipoDato(self.tipo)))

        if self.valor != None:
            if isinstance(self.valor,list):
                expresionsNode = NodeCst("expresion")
                expresionsNode.addChild(str(self.value))
                nodo.addChildNode(expresionsNode)
            else:
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