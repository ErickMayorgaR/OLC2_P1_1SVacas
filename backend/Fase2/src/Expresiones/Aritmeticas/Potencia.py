from typing import NewType
from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class Potencia(Instruccion):
    def __init__(self, opIzq, opDer, fila, columna):
        self.opIzq = opIzq
        self.opDer = opDer
        self.tipo = None
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        opIzq = self.opIzq.interpretar(tree, table, generator)
        if isinstance(opIzq, Excepcion):
            return opIzq

        opDer = self.opDer.interpretar(tree, table, generator)
        if isinstance(opDer, Excepcion):
            return opDer

        newTemp = generator.createTemp()

        return self.potenciar(opIzq, opDer, newTemp, tree, table, generator)
    
    def getNode(self):
        return super().getNode()

    def potenciar(self, opIzq, opDer, newTemp, tree, table, generator):
        #INT
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return self.C3DPotencia(opIzq, opDer, newTemp, table, tree, generator)

        #STRING
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.CADENA
            valIzq = self.correctValue(opIzq)
            valDer = self.correctValue(opDer)
            return self.elevarString(valIzq, valDer, newTemp, tree, table, generator)

        return Excepcion("Semántico", "Los tipos de datos para el signo \"^\" no pueden ser operados", self.fila, self.columna)

    def C3DPotencia(self, opIzq, opDer, newTemp, table, tree, generator):
        newTempAmbitoSimulado = generator.createTemp()
        tree.updateConsola(generator.newSimulateNextStack(newTempAmbitoSimulado, str(table.size)))

        newTempIndiceBase = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceBase, newTempAmbitoSimulado, '1', '+'))
        base = self.correctValue(opIzq)
        tree.updateConsola(generator.newSetStack(newTempIndiceBase, str(base)))

        newTempIndiceExponente = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceExponente, newTempAmbitoSimulado, '2', '+'))
        exponente = self.correctValue(opDer)
        tree.updateConsola(generator.newSetStack(newTempIndiceExponente, str(exponente)))

        tree.updateConsola(generator.newNextStack(str(table.size)))
        tree.updateConsola(generator.newCallFunc('Potencia_armc'))

        newTempIndiceReturn = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceReturn, 'P', '0', '+'))

        tree.updateConsola(generator.newGetStack(newTemp, newTempIndiceReturn))

        tree.updateConsola(generator.newBackStack(str(table.size)))

        valor = Value(1, newTemp, self.tipo, True)
        return valor


    def elevarString(self, opIzq, opDer, newTemp, tree, table, generator):
        newTempAmbitoSimulado = generator.createTemp()
        tree.updateConsola(generator.newSimulateNextStack(newTempAmbitoSimulado, str(table.size))) #Cambio simulado de ambito

        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, newTempAmbitoSimulado, '1', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam1Indice, str(opIzq)))

        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, newTempAmbitoSimulado, '2', '+'))
        tree.updateConsola(generator.newSetStack(newTempParam2Indice, str(opDer)))    

        tree.updateConsola(generator.newNextStack(str(table.size)))

        tree.updateConsola(generator.newCallFunc('Elevar_String_armc'))

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