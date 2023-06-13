from ..Abstract.abstract import Instruccion
from ..TS.Tipo import OperadorLogico, Tipo
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion

class Logica(Instruccion):
    def __init__(self, operador, opIzq, opDer, fila, columna):
        self.operador = operador
        self.opIzq = opIzq
        self.opDer = opDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        opIzq = self.opIzq.interpretar(tree, table)
        if isinstance(opIzq, Excepcion):
            return opIzq

        if self.opDer != None:
            opDer = self.opDer.interpretar(tree, table)
            if isinstance(opDer, Excepcion):
                return opDer

        #and
        if self.operador == OperadorLogico.AND:
            return self.And(opIzq, opDer)

        #or
        elif self.operador == OperadorLogico.OR:
            return self.Or(opIzq, opDer)

        #not
        elif self.operador == OperadorLogico.NOT:
            return self.Not(opIzq)

        return Excepcion("Semántico", "Tipo de operación lógica no Especificado.", self.fila, self.columna)


    def And(self, opIzq, opDer):
        if self.opIzq.tipo == Tipo.BANDERA and self.opDer.tipo == Tipo.BANDERA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) and self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"&&\" no son los correctos", self.fila, self.columna)

    
    def Or(self, opIzq, opDer):
        if self.opIzq.tipo == Tipo.BANDERA and self.opDer.tipo == Tipo.BANDERA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) or self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"||\" no son los correctos", self.fila, self.columna)


    def Not(self, opIzq):
        if self.opIzq.tipo == Tipo.BANDERA:
            self.tipo = Tipo.BANDERA
            return not self.getType(self.opIzq, opIzq)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"!\" no son los correctos", self.fila, self.columna)


    def getType(self, nodo, valor):
        if nodo.tipo == Tipo.NUMBER:
            return int(valor)
        elif nodo.tipo == Tipo.DOBLE:
            return float(valor)
        elif nodo.tipo == Tipo.CADENA:
            return str(valor)
        elif nodo.tipo == Tipo.BANDERA:
            if str(valor).lower() == 'true':
                return True
            elif str(valor).lower() == 'false':
                return False
        elif nodo.tipo == Tipo.CARACTER:
            return str(valor)
        return valor

    def getNode(self):
        nodo = NodeCst("expresion")
        nodo.addChildNode(self.opIzq.getNode())
        nodo.addChild(str(self.tipoOperador(self.operador)))
        if self.opDer != None:
            nodo.addChildNode(self.opDer.getNode())
        return nodo


    
    def tipoOperador(self, op):
        if op == OperadorLogico.NOT:
            return '!'
        elif op == OperadorLogico.AND:
            return '&&'
        elif op == OperadorLogico.OR:
            return '||'