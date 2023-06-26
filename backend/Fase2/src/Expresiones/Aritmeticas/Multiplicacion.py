from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class Multiplicacion(Instruccion):
    def __init__(self, opIzq, opDer, fila, columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table, generator):
        opIzq = self.opIzq.interpretar(tree, table, generator)
        if isinstance(opIzq, Excepcion):
            return opIzq

        opDer = self.opDer.interpretar(tree, table, generator)
        if isinstance(opDer, Excepcion):
            return opDer

        newTemp = generator.createTemp()

        return self.multiplicar(opIzq, opDer, newTemp, tree, table, generator)

    def getNode(self):
        return super().getNode()

    def multiplicar(self, opIzq, opDer, newTemp, tree, table, generator):
        valIzq = self.correctValue(opIzq)
        valDer = self.correctValue(opDer)
        #INT
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            tree.updateConsola(generator.newExpresion(newTemp, str(valIzq), str(valDer), "*"))
            self.tipo = Tipo.NUMBER
            valor = 1
            newValue = Value(valor, newTemp, self.tipo, True)
            return newValue

        #STRING
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.CADENA
            return self.concatenacion(valIzq, valDer, newTemp, tree, table, generator)
            
        return Excepcion("Semántico", "Los tipos de datos para el signo \"*\" no pueden ser operados", self.fila, self.columna)


    def concatenacion(self, opIzq, opDer, newTemp, tree, table, generator):
        newTempAmbitoSimulado = generator.createTemp()
        tree.updateConsola(generator.newSimulateNextStack(newTempAmbitoSimulado, str(table.size))) #Cambio simulado de ambito

        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, newTempAmbitoSimulado, '1', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam1Indice, str(opIzq)))

        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, newTempAmbitoSimulado, '2', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam2Indice, str(opDer)))    

        tree.updateConsola(generator.newNextStack(str(table.size)))

        tree.updateConsola(generator.newCallFunc('Concatenar_String_armc'))

        newTempReturn = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturn, 'P', '0', '+'))
        tree.updateConsola(generator.newGetStack(newTemp, newTempReturn))

        tree.updateConsola(generator.newBackStack(str(table.size)))

        newValue = Value('', newTemp, self.tipo, True)
        return newValue

    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()