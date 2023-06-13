from ...Abstract.abstract import Instruccion

class DeclaracionArreglos(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return super().interpretar(tree, table)

    def getNode(self):
        pass