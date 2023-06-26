from ..Instrucciones.Variables.Asignacion import AsignacionVar

from ..Expresiones.Primitivos.Number import Number
from ..Instrucciones.Funcion.Funcion import Funcion
from ..TS.Tipo import Tipo

class FuncPotencia(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO

    def interpretar(self, tree, table, generator):
        tree.updateConsola("\nfunc Potencia_armc(){\n")

        newTempIndiceI = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceI, 'P', '3', '+'))
        tree.updateConsola(generator.newSetStack(newTempIndiceI, '0'))

        newTempIndiceRes = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceRes, 'P', '4', '+'))
        tree.updateConsola(generator.newSetStack(newTempIndiceRes, '1'))

        newLabelRecursivo = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo))

        newTempIndiceI2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceI2, 'P', '3', '+'))
        newTempIValor2 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempIValor2, newTempIndiceI2))

        newTempIndiceExponente = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceExponente, 'P', '2', '+'))
        newTempExponenteValor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempExponenteValor, newTempIndiceExponente))

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempIValor2, newTempExponenteValor, '<', trueLabel))

        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))

        newTempIndiceRes3 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceRes3, 'P', '4', '+'))
        newTempValorRes3 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempValorRes3, newTempIndiceRes3))

        newTempIndiceBase = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceBase, 'P', '1', '+'))
        newTempValorBase = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempValorBase, newTempIndiceBase))

        newTempMultiplicacion = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempMultiplicacion, newTempValorRes3, newTempValorBase, '*'))

        newTempIndiceRes2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceRes2, 'P', '4', '+'))

        tree.updateConsola(generator.newSetStack(newTempIndiceRes2, newTempMultiplicacion))

        newTempIndiceI3 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceI3, 'P', '3', '+'))
        newTempIValor3 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempIValor3, newTempIndiceI3))

        newTempSuma = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempSuma, newTempIValor3, '1', '+'))

        newTempIndiceI4 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceI4, 'P', '3', '+'))

        tree.updateConsola(generator.newSetStack(newTempIndiceI4, newTempSuma))
        
        tree.updateConsola(generator.newGoto(newLabelRecursivo))

        tree.updateConsola(generator.newLabel(falseLabel))

        newTempIndiceRes4 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceRes4, 'P', '4', '+'))
        newTempValorRes4 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempValorRes4, newTempIndiceRes4))

        
        newTempIndiceReturn = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempIndiceReturn, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempIndiceReturn, newTempValorRes4))


        tree.updateConsola(generator.newReturn())
        tree.updateConsola("}")


    def getNode(self):
        return super().getNode()