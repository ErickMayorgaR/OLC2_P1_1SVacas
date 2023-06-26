from ...Abstract.abstract import Instruccion

class Continue(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table, generator):
        tree.updateConsola(generator.newGoto(str(self.label)))
        tree.updateConsola(generator.newPrint('c', '13'))
        return self

    def getNode(self):
        return super().getNode()