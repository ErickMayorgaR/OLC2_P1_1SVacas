from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class MayorIgual(Instruccion):
    def __init__(self, opIzq, opDer, fila, columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.tipo = None
        self.trueLabel = None
        self.falseLabel = None
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table, generator):
        opIzq = self.opIzq.interpretar(tree, table, generator)
        if isinstance(opIzq, Excepcion):
            return opIzq

        opDer = self.opDer.interpretar(tree, table, generator)
        if isinstance(opDer, Excepcion):
            return opDer

        return self.esMayorIgual(opIzq, opDer, tree, table, generator)

    def getNode(self):
        return super().getNode()

    def esMayorIgual(self, opIzq, opDer, tree, table, generator):
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.returnValue(opIzq, opDer, tree, generator)

        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            valIzq = self.correctValue(opIzq)
            valDer = self.correctValue(opDer)
            newTemp = generator.createTemp()
            return self.mayorIgualCadena(newTemp, valIzq, valDer, tree, table, generator)

        return Excepcion("Semántico", "Los tipos de datos para el signo \">=\" no pueden ser operados", self.fila, self.columna)


    def returnValue(self, opIzq, opDer, tree, generator):
        valIzq = self.correctValue(opIzq)
        valDer = self.correctValue(opDer)
        valor = True
        newValue = Value(valor, "", self.tipo, False)
            
        if self.trueLabel == None:
            self.trueLabel = generator.createLabel()

        if self.falseLabel == None:
            self.falseLabel = generator.createLabel()

        tree.updateConsola(generator.newIf(str(valIzq), str(valDer), '>=', self.trueLabel))
        tree.updateConsola(generator.newGoto(self.falseLabel))

        newValue.trueLabel = self.trueLabel
        newValue.falseLabel = self.falseLabel

        return newValue

    def mayorIgualCadena(self, newTemp, opIzq, opDer, tree, table, generator):
        newTempAmbitoSimulado = generator.createTemp()
        tree.updateConsola(generator.newSimulateNextStack(newTempAmbitoSimulado, str(table.size))) #Cambio simulado de ambito

        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, newTempAmbitoSimulado, '1', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam1Indice, str(opIzq)))

        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, newTempAmbitoSimulado, '2', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam2Indice, str(opDer)))    

        tree.updateConsola(generator.newNextStack(str(table.size)))

        tree.updateConsola(generator.newCallFunc('String_Mayor_Igual_armc'))

        newTempReturn = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturn, 'P', '0', '+'))
        tree.updateConsola(generator.newGetStack(newTemp, newTempReturn))

        tree.updateConsola(generator.newBackStack(str(table.size)))

        if self.trueLabel == None:
            self.trueLabel = generator.createLabel()

        if self.falseLabel == None:
            self.falseLabel = generator.createLabel()

        newValue = Value('', newTemp, self.tipo, True)

        tree.updateConsola(generator.newIf(newTemp, '1', '==', self.trueLabel))
        tree.updateConsola(generator.newGoto(self.falseLabel))

        newValue.trueLabel = self.trueLabel
        newValue.falseLabel = self.falseLabel
        return newValue

    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()