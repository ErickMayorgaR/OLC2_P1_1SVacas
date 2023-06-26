from ..Instrucciones.Funcion.Funcion import Funcion

class ElevarString(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        tree.updateConsola("\nfunc Elevar_String_armc(){\n")

        newTempParam2Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam2Indice, 'P', '2', '+'))
        newTempParam2Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam2Valor, newTempParam2Indice))

        newTempContadorIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContadorIndice, 'P', '3', '+'))
        tree.updateConsola(generator.newSetStack(newTempContadorIndice, '0'))

        newTempStartStringIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempStartStringIndice, 'P', '4', '+'))
        tree.updateConsola(generator.newSetStack(newTempStartStringIndice, 'H'))

        newTempContadorIndice2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempContadorIndice2, 'P', '3', '+'))
        newTempContadorValor2 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempContadorValor2, newTempContadorIndice2))

        #Empieza primer while
        newLabelRecursivo = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo))

        trueLabel = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempContadorValor2, newTempParam2Valor, '<', trueLabel))
        falseLabel = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel))

        tree.updateConsola(generator.newLabel(trueLabel))

        newTempParam1Indice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempParam1Indice, 'P', '1', '+'))
        newTempParam1Valor = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempParam1Valor, newTempParam1Indice))

        #Empieza primer while2
        newLabelRecursivo2 = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabelRecursivo2))

        newTempCaracter = generator.createTemp()
        tree.updateConsola(generator.newGetHeap(newTempCaracter, newTempParam1Valor))

        trueLabel2 = generator.createLabel()
        tree.updateConsola(generator.newIf(newTempCaracter, '-1', '!=', trueLabel2))
        falseLabel2 = generator.createLabel()
        tree.updateConsola(generator.newGoto(falseLabel2))

        tree.updateConsola(generator.newLabel(trueLabel2))
        tree.updateConsola(generator.newSetHeap('H', newTempCaracter))
        tree.updateConsola(generator.newNextHeap())

        tree.updateConsola(generator.newExpresion(newTempParam1Valor, newTempParam1Valor, '1', '+'))
        
        tree.updateConsola(generator.newGoto(newLabelRecursivo2))

        tree.updateConsola(generator.newLabel(falseLabel2))

        tree.updateConsola(generator.newExpresion(newTempContadorValor2, newTempContadorValor2, '1', '+'))
        
        tree.updateConsola(generator.newGoto(newLabelRecursivo))

        tree.updateConsola(generator.newLabel(falseLabel))

        #---------------------------------------------------------------------------
        tree.updateConsola(generator.newSetHeap('H', '-1'))
        tree.updateConsola(generator.newNextHeap())

        #Valor del return 
        newTempStartStringIndice2 = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempStartStringIndice2, 'P', '4', '+'))
        newTempStartStringValor2 = generator.createTemp()
        tree.updateConsola(generator.newGetStack(newTempStartStringValor2, newTempStartStringIndice2))


        newTempReturnIndice = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempReturnIndice, 'P', '0', '+'))
        tree.updateConsola(generator.newSetStack(newTempReturnIndice, newTempStartStringValor2))

        tree.updateConsola(generator.newReturn())
        tree.updateConsola("}")
    def getNode(self):
        return super().getNode()