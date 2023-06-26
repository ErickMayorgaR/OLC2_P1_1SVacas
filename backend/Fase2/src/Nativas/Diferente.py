from ..Instrucciones.Funcion.Funcion import Funcion

class StringDiferente(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        tree.updateConsola("\nfunc String_Diferente_armc(){\n")
        #Cadena 1
        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, 'P', '1', '+'))
        newTempParam1Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam1Valor, newTempParam1Indice))

        #Cadena 2
        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, 'P', '2', '+'))
        newTempParam2Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam2Valor, newTempParam2Indice))

        outLabel = generator.createLabel()
        #Empieza primer while
        newLabelRecursivo = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo))

        newTempCaracterParam1 = generator.createTemp()
        tree.updateConsola(generator.newGetHeap(newTempCaracterParam1, newTempParam1Valor))

        newTempCaracterParam2 = generator.createTemp()
        tree.updateConsola(generator.newGetHeap(newTempCaracterParam2, newTempParam2Valor))

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempCaracterParam1, newTempCaracterParam2, '!=', trueLabel))
        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))

        newTempReturnIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturnIndice, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempReturnIndice, '1'))
        tree.updateConsola(generator.newGoto(outLabel))


        tree.updateConsola(generator.newLabel(falseLabel))

        trueLabelMenosUno = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempCaracterParam1, '-1', '==', trueLabelMenosUno))
        falseLabelMenosUno = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabelMenosUno))

        tree.updateConsola(generator.newLabel(trueLabelMenosUno))
        newTempReturnIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturnIndice, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempReturnIndice, '0'))
        tree.updateConsola(generator.newGoto(outLabel))

        tree.updateConsola(generator.newLabel(falseLabelMenosUno))
        tree.updateConsola(generator.newExpresion(newTempParam1Valor, newTempParam1Valor, '1', '+'))
        tree.updateConsola(generator.newExpresion(newTempParam2Valor, newTempParam2Valor, '1', '+'))

        tree.updateConsola(generator.newGoto(newLabelRecursivo))


        tree.updateConsola(generator.newLabel(outLabel))
        tree.updateConsola(generator.newReturn())
        tree.updateConsola("}")

    def getNode(self):
        return super().getNode()