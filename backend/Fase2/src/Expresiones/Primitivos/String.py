from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class String(Instruccion):
    def __init__(self, valor, tipo, fila, columna):
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        if self.tipo != Tipo.CADENA:
            return Excepcion("Semántico", "El valor no es tipo STRING", self.fila, self.columna)

        string = Value(str(self.valor), "", self.tipo, False)

        newTemp = generator.createTemp() 

        self.addCadena(string, newTemp, table.size , tree, generator)

        return Value(str(self.valor), newTemp, self.tipo, True)


    def getNode(self):
        return super().getNode()

    def addCadena(self, value, newTempH, tamTable, tree, generator):
        tree.updateConsola(generator.newAsigTemp(newTempH, 'H'))
        for char in value.getValor():
            tree.updateConsola(generator.newSetHeap('H', str(ord(char))))
            tree.updateConsola(generator.newNextHeap())
        tree.updateConsola(generator.newSetHeap('H', str(-1)))
        tree.updateConsola(generator.newNextHeap())