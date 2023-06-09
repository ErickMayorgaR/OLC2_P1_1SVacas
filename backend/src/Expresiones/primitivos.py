from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst

class Primitivos(Instruccion):

    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        return self.valor


    def getNode(self):
        nodo = NodeCst("expresion")
        nodo.addChild(str(self.valor))
        return nodo