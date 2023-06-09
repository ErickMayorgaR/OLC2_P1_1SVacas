from datetime import datetime

class Excepcion:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.now = datetime.now()
        self.fecha = self.getFecha()
        self.hora = self.getHora()

    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + str(self.fila) + ", " + str(self.columna) + "]" + " - " + str(self.fecha) + " - " + str(self.hora)

    def getFecha(self):
        return str(self.now.day)+"-"+str(self.now.month)+"-"+str(self.now.year) 

    def getHora(self):
        return str(self.now.hour)+":"+str(self.now.minute)