from ..Instrucciones.Funcion.Funcion import Funcion

class StringMayorIgual(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        tree.updateConsola("\nfunc String_Mayor_Igual_armc(){\n")

        #Cadena 1
        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, 'P', '1', '+'))
        newTempParam1Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam1Valor, newTempParam1Indice))

        newTempContadorIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContadorIndice, 'P', '3', '+'))
        tree.updateConsola(generator.newSetStack(newTempContadorIndice, '0'))

        newTempContadorIndice2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContadorIndice2, 'P', '3', '+'))
        newTempContadorValor2 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempContadorValor2, newTempContadorIndice2))

        #Empieza primer while
        newLabelRecursivo = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo))

        newTempCaracterParam1 = generator.createTemp()
        tree.updateConsola(generator.newGetHeap(newTempCaracterParam1, newTempParam1Valor))

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempCaracterParam1, '-1', '!=', trueLabel))
        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))

        tree.updateConsola(generator.newExpresion(newTempParam1Valor, newTempParam1Valor, '1', '+'))
        tree.updateConsola(generator.newExpresion(newTempContadorValor2, newTempContadorValor2, '1', '+'))

        tree.updateConsola(generator.newGoto(newLabelRecursivo))

        tree.updateConsola(generator.newLabel(falseLabel))

        #Cadena 2
        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, 'P', '2', '+'))
        newTempParam2Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam2Valor, newTempParam2Indice))

        newTempContador2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContador2Indice, 'P', '4', '+'))
        tree.updateConsola(generator.newSetStack(newTempContador2Indice, '0'))

        newTempContador2Indice2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContador2Indice2, 'P', '4', '+'))
        newTempContador2Valor2 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempContador2Valor2, newTempContador2Indice2))

        #Empieza segundo while
        newLabelRecursivo = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo))

        newTempCaracterParam1 = generator.createTemp()
        tree.updateConsola(generator.newGetHeap(newTempCaracterParam1, newTempParam2Valor))

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempCaracterParam1, '-1', '!=', trueLabel))
        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))

        tree.updateConsola(generator.newExpresion(newTempParam2Valor, newTempParam2Valor, '1', '+'))
        tree.updateConsola(generator.newExpresion(newTempContador2Valor2, newTempContador2Valor2, '1', '+'))

        tree.updateConsola(generator.newGoto(newLabelRecursivo))

        tree.updateConsola(generator.newLabel(falseLabel))

        #Comparacion de tamanos
        outLabel = generator.createLabel()

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempContadorValor2, newTempContador2Valor2, '>=', trueLabel))
        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))
        newTempReturnIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturnIndice, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempReturnIndice, '1'))
        tree.updateConsola(generator.newGoto(outLabel))

        tree.updateConsola(generator.newLabel(falseLabel))
        newTempReturnIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturnIndice, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempReturnIndice, '0'))
        tree.updateConsola(generator.newGoto(outLabel))

        tree.updateConsola(generator.newLabel(outLabel))
        tree.updateConsola(generator.newReturn())
        tree.updateConsola("}")

    def getNode(self):
        return super().getNode()