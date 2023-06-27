from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from copy import copy

class ModificacionArreglo(Instruccion):
    def __init__(self, identificador, dimensiones, expresiones, fila, columna):
        self.identificador = identificador
        self.dimensiones = dimensiones
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.value = ""

    def interpretar(self, tree, table):
        if isinstance(self.expresiones, list):
            value = copy(self.expresiones)
            self.copiarArreglo(value, self.expresiones)
            val = self.interpretarArreglos(tree, table, value)
            if isinstance(val, Excepcion):
                return val
        else:
            value = self.expresiones.interpretar(tree, table)
        
        self.value = value

        simbolo = table.getTabla(str(self.identificador))
        if simbolo == None:
            return Excepcion("Semántico", "Arreglo \""+self.identificador+"\" no encontrado", self.fila, self.columna)

        if simbolo.getTipo() != 'array':
            return Excepcion("Semántico", "La varible \""+str(self.identificador)+"\" a la que intenta acceder no es un arreglo", self.fila, self.columna)

        valueResult = self.modify(tree, table, copy(self.dimensiones), simbolo.getValor(), value)
        if isinstance(valueResult, Excepcion):
            return valueResult
        
        return valueResult


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


    def modify(self, tree, table, dimensiones, arreglo, valor):
        if len(dimensiones) == 0:
            if isinstance(arreglo, list):
                return Excepcion("Semántico", "Acceso de mas en un arreglo", self.fila, self.columna)
            return valor
        
        if not(isinstance(arreglo, list)):
            return Excepcion("Semántico", "Acceso de mas en un arreglo", self.fila, self.columna)

        dimension = dimensiones.pop(0)
        
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion):
            return num
        
        if num == 0:
            return Excepcion("Semántico", "Indice en arreglo \""+self.identificador+"\" fuera de rango", self.fila, self.columna)

        
        if dimension.tipo != 'number':
            return Excepcion("Semántico", "Expresion diferente a ENTERO en Arreglo", self.fila, self.columna)

        try:
            valor = self.modify(tree, table, copy(dimensiones), arreglo[num-1], valor)
        except:
            return Excepcion("Semántico", "Indice en arreglo \""+self.identificador+"\" fuera de rango", self.fila, self.columna)

        if isinstance(valor, Excepcion):
            return valor

        if valor != None:
            arreglo[num-1] = valor

        return None       

    def getNode(self):
        nodo = NodeCst("modificar_arreglo")
        nodo.addChild(str(self.identificador))
        dimentionsNode = NodeCst("lista_dimensiones")
        for dimension in self.dimensiones:
            dimentionsNode.addChildNode(dimension.getNode())
        nodo.addChildNode(dimentionsNode)
        expresionsNode = NodeCst("expresion")
        expresionsNode.addChild(str(self.value))
        nodo.addChildNode(expresionsNode)
        return nodo