from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNode(self):
        nodo = NodeCst("break_instr")
        nodo.addChild("BREAK")
        return nodo