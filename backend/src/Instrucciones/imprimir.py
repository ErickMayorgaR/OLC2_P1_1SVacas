from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst

class Imprimir(Instruccion):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion # <<Class.Primitivos>>
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        print(value)
        return value
    
    def getNode(self):
        nodo = NodeCst("imprimir_instr")
        if isinstance(self.expresiones, list):
            for expresion in self.expresiones:
                nodo.addChildNode(expresion.getNode())
        elif self.expresiones == None:
            nodo.addChild("")    
        else:
            nodo.addChildNode(self.expresiones.getNode())    
        return nodo