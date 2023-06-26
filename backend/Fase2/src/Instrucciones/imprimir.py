from ..Abstract.abstract import Instruccion
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import Tipo


class Imprimir(Instruccion):
    def __init__(self, expresiones, saltoLinea, fila, columna):
        self.expresiones = expresiones
        self.saltoLinea = saltoLinea
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        if isinstance(self.expresiones, list): 
            for expresion in self.expresiones:
                result = self.print(expresion, tree, table, generator)
                if isinstance(result, Excepcion):
                    return result

        else:
            tree.updateConsola(generator.newPrint("c", '00'))

        if self.saltoLinea:
            tree.updateConsola(generator.newNewLine())   

        return None   

    def getNode(self):
        return super().getNode()

    def print(self, expresion, tree, table, generator):
        tempValor = expresion.interpretar(tree, table, generator)
        if isinstance(tempValor, Excepcion):
            return tempValor

        valor = self.correctValue(tempValor)

        if tempValor.getTipo() == Tipo.NUMBER:  #Imprime enteros
            tree.updateConsola(generator.newPrint("d", "int(" + str(valor) + ")"))
                    
        elif tempValor.tipo == Tipo.CADENA:                     #Imprime strings 
            self.printString(valor, tree, table, generator)

        elif tempValor.tipo == Tipo.BANDERA:                    #Imprime booleans
            trueIns = generator.newCallFunc('print_true_armc')
            falseIns = generator.newCallFunc('print_false_armc')
            tree.updateConsola(generator.newOpRelacional(tempValor, trueIns, falseIns))
            
        else:
            return Excepcion("Semántico", "No se puede imprimir una variable " + str(tempValor.getTipo()), self.fila, self.columna)

    def printString(self, valor, tree, table, generator):
        newTempCambioSimulado = generator.createTemp()                                             
        tree.updateConsola(generator.newSimulateNextStack(newTempCambioSimulado, str(table.size))) #Cambio simulado de entorno
        newTempGuardarParam = generator.createTemp()
        tree.updateConsola(generator.newExpresion(newTempGuardarParam, newTempCambioSimulado, '1', '+'))
        tree.updateConsola(generator.newSetStack(newTempGuardarParam, str(valor)))
        tree.updateConsola(generator.newNextStack(str(table.size))) #Cambio de entorno real
        tree.updateConsola(generator.newCallFunc('Print_String_armc')) #Llamada de funcion
        tree.updateConsola(generator.newBackStack(str(table.size))) #Regreso de ambito

    
    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()