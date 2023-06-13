from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion

class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)

        if simbolo == None:
            return Excepcion("Semántico", "La variable \""+self.identificador+"\" no existe", self.fila, self.columna)
        
        self.tipo = simbolo.getTipo()

        return simbolo.getValor()

    def getNode(self):
        nodo = NodeCst("expresion")
        nodo.addChild(str(self.identificador))
        return nodo