from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import Tipo

class String(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO

    def interpretar(self, tree, table):
        expresion = self.expresion.interpretar(tree, table)
        if isinstance(expresion, Excepcion):
            return expresion

        self.tipo = Tipo.CADENA

        if self.expresion.tipo == Tipo.NUMBER:
            try:
                return str(int(expresion))
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)
        #string a string
        elif self.expresion.tipo == Tipo.CADENA:
            try:
                return str(expresion)
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)

        #double a string
        elif self.expresion.tipo == Tipo.DOBLE:
            try:
                return str(float(expresion))
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)
        #char a string
        elif self.expresion.tipo == Tipo.CARACTER:
            try:
                return str(expresion)
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)
        #boolean a string
        elif self.expresion.tipo == Tipo.BANDERA:
            try:
                return str(expresion)
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)
        #arreglar a string
        elif self.expresion.tipo == Tipo.ARREGLO:
            try:
                return str(expresion)
            except:
                return Excepcion("Semántico", "No se puede castear para STRING", self.fila, self.columna)

        return Excepcion("Semántico", "Parametro de funcion string erroneo", self.fila, self.columna)
        
    def getNode(self):
        nodo = NodeCst("nativas_instr")
        nodo.addChild("STRING")
        nodo.addChildNode(self.expresion.getNode())
        return nodo