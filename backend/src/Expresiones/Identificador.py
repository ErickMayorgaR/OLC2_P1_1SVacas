from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion

class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna, tipo = None):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)

        if simbolo == None:
            return Excepcion("Semántico", "La variable \""+self.identificador+"\" no existe", self.fila, self.columna)
        
        self.tipo = simbolo.getTipo()

        return simbolo.getValor()

    def getTipo(self):
        return self.tipo
    
    def getNode(self):
        nodo = NodeCst("expresion")
        nodo.addChild(str(self.identificador))
        return nodo