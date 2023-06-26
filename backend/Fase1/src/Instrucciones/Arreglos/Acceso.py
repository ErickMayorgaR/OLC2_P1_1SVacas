from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo
from copy import copy

class AccesoArreglo(Instruccion):
    def __init__(self, identificador, dimensiones, fila, columna):
        self.identificador = identificador
        self.dimensiones = dimensiones
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO

    def interpretar(self, tree, table):
        simbolo = table.getTabla(str(self.identificador))
        if simbolo == None:
            return Excepcion("Semántico", "Arreglo \""+self.identificador+"\" no encontrado", self.fila, self.columna)

        if simbolo.getTipo() != Tipo.ARREGLO:
            return Excepcion("Semántico", "La varible \""+str(self.identificador)+"\" a la que intenta acceder no es un arreglo", self.fila, self.columna)

        value = self.findDimentions(tree, table, copy(self.dimensiones), simbolo.getValor())
        if isinstance(value, Excepcion):
            return value
        #if isinstance(value, list):
            #return Excepcion("Semántico", "Acceso a arreglo incompleto", self.fila, self.columna)
        
        self.tipoDato(value)

        return value

    def tipoDato(self, value):
        if isinstance(value, int):
            self.tipo = Tipo.NUMBER
        elif isinstance(value, float):
            self.tipo = Tipo.DOBLE
        elif isinstance(value, str):
            if len(value) == 1:
                self.tipo = Tipo.CARACTER
            else:
                self.tipo = Tipo.CADENA
        elif isinstance(value, bool):
            self.tipo = Tipo.BANDERA
        elif isinstance(value, list):
            self.tipo = Tipo.ARREGLO

    def findDimentions(self, tree, table, dimensiones, arreglo):
        value = None
        if len(dimensiones) == 0:
            return arreglo
        
        '''if not(isinstance(arreglo, list)):
            return Excepcion("Semántico", "Acceso de mas en un arreglo", self.fila, self.columna)'''
        dimension = dimensiones.pop(0)
        num = dimension.interpretar(tree, table)
        
        if isinstance(num, Excepcion):
            return num

        if num == 0:
            return Excepcion("Semántico", "Indice en arreglo \""+self.identificador+"\" fuera de rango", self.fila, self.columna)
        
        if dimension.tipo != Tipo.NUMBER:
            return Excepcion("Semántico", "Expresión diferente a ENTERO en Arreglo", self.fila, self.columna)
        
        try:
            value = self.findDimentions(tree, table, copy(dimensiones), arreglo[num-1])
        except:
            return Excepcion("Semántico", "Indice en arreglo \""+self.identificador+"\" fuera de rango", self.fila, self.columna)

        return value

    def getNode(self):
        nodo = NodeCst("acceso_arreglo")
        nodo.addChild(str(self.identificador))
        dimentionsNode = NodeCst("lista_dimensiones")
        for dimension in self.dimensiones:
            dimentionsNode.addChildNode(dimension.getNode())
        nodo.addChildNode(dimentionsNode)
        return nodo