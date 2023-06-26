class Simbolo:
    def __init__(self, identificador, tipo, valor, posicion, local, globall, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
        self.posicion = posicion
        self.local = local
        self.globall = globall
        self.fila = fila
        self.columna = columna

    def getID(self):
        return self.identificador

    def serID(self, identificador):
        self.identificador = identificador

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo 

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getPosicion(self):
        return self.posicion

    def setPosicion(self, posicion):
        self.posicion = posicion

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def getLocal(self):
        return self.local

    def getGloball(self):
        return self.globall