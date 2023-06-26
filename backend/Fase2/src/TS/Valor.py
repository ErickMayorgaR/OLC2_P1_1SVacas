class Value:
    def __init__(self, valor, temporal, tipo, isTemp):
        self.valor = valor
        self.temporal = temporal
        self.tipo = tipo
        self.isTemp = isTemp
        self.trueLabel = None
        self.falseLabel = None

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = str(valor)

    def getTemporal(self):
        return self.temporal

    def setTemporal(self, temporal):
        self.temporal = str(temporal)

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getIsTemp(self):
        return self.isTemp

    def getTrueLabel(self):
        return self.trueLabel

    def getFalseLabel(self):
        return self.falseLabel