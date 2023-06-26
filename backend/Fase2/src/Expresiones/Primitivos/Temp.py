from ...Abstract.abstract import Instruccion

class Temporal(Instruccion):
    def __init__(self, valor, fila, columna):
        self.valor = valor
        self.tipo = None
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        self.tipo = self.valor.tipo
        return self.valor

    def getNode(self):
        return super().getNode()