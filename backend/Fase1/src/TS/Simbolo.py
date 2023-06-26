class Simbolo:
    def __init__(self, identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def getID(self):
        return self.identificador

    def setID(self, id):
        self.identificador = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor 

    def getFila(self):
        return self.fila
    
    def setFila(self,fila):
        self.fila = fila

    def getColumna(self):
        return self.columna

    def setColumna(self,columna):
        self.columna = columna