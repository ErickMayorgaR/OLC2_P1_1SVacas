from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo
from copy import copy

class Not(Instruccion):
    def __init__(self, opIzq, fila, columna):
        self.opIzq = opIzq
        self.tipo = None
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        opIzq = self.opIzq.interpretar(tree, table, generator)
        if isinstance(opIzq, Excepcion):
            return opIzq

        if self.opIzq.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "Los tipos de datos para el signo \"!\" no pueden ser operados", self.fila, self.columna)

        self.tipo = Tipo.BANDERA
        
        trueLabels = copy(opIzq.trueLabel)
        falseLabels = copy(opIzq.falseLabel)

        opIzq.trueLabel = falseLabels
        opIzq.falseLabel = trueLabels

        return opIzq

    def getNode(self):
        return super().getNode()