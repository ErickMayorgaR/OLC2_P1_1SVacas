from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class Boolean(Instruccion):
    def __init__(self, valor, tipo, fila, columna):
        self.valor = valor
        self.tipo = tipo
        self.trueLabel = None
        self.falseLabel = None
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        if self.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "El valor no es tipo BOOLEAN", self.fila, self.columna)
        
        if str(self.valor).lower() == 'true':
            newValue = Value(1, "", self.tipo, False)
        else:
            newValue = Value(0, "", self.tipo, False)
        if self.trueLabel == None:
            self.trueLabel = generator.createLabel()

        if self.falseLabel == None:
            self.falseLabel = generator.createLabel()

        tree.updateConsola(generator.newIf(str(newValue.getValor()), '1', '==', self.trueLabel))
        tree.updateConsola(generator.newGoto(self.falseLabel))

        newValue.trueLabel = self.trueLabel
        newValue.falseLabel = self.falseLabel

        return newValue

    def getNode(self):
        return super().getNode()