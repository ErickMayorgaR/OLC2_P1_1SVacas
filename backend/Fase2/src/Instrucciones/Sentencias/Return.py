from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo

class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
        self.result = None
        self.label = ''

    def interpretar(self, tree, table, generator):
        if self.expresion == None:
            tree.updateConsola(generator.newGoto(str(self.label)))
            tree.updateConsola(generator.newPrint('c', '13'))
            self.tipo = Tipo.NULO
            return 

        resultExpresion = self.expresion.interpretar(tree, table, generator)
        if isinstance(resultExpresion, Excepcion):
            return resultExpresion

        value = self.correctValue(resultExpresion)

        newTemp = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTemp, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTemp, str(value)))
        self.tipo = resultExpresion.getTipo()
        return self

    def getNode(self):
        return super().getNode()

    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()