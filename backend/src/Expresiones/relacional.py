from ..Abstract.abstract import Instruccion
from ..TS.Tipo import OperadorRelacional, Tipo
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion


class Relacional(Instruccion):
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

        #igualacion
        if self.operador == OperadorRelacional.IGUALIGUAL:
            return self.igualacion(opIzq, opDer)

        #diferente
        elif self.operador == OperadorRelacional.DIFERENTE:
            return self.diferencia(opIzq, opDer)

        #menor que
        elif self.operador == OperadorRelacional.MENOR:
            return self.menor(opIzq, opDer)

        #mayor que
        elif self.operador == OperadorRelacional.MAYOR:
            return self.mayor(opIzq, opDer)

        #menor igual
        elif self.operador == OperadorRelacional.MENORIGUAL:
            return self.menorIgual(opIzq, opDer)

        #mayor igual
        elif self.operador == OperadorRelacional.MAYORIGUAL:
            return self.mayorIgual(opIzq, opDer)
        
        return Excepcion("Semántico", "Tipo de operación relacional no Especificado.", self.fila, self.columna)


    def igualacion(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.BANDERA and self.opDer.tipo == Tipo.BANDERA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NULO and self.opDer.tipo == Tipo.NULO):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.NULO or self.opDer.tipo == Tipo.NULO:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) == self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"==\" no son los correctos", self.fila, self.columna)
    

    def diferencia(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.BANDERA and self.opDer.tipo == Tipo.BANDERA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NULO and self.opDer.tipo == Tipo.NULO):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.NULO or self.opDer.tipo == Tipo.NULO:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) != self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"!=\" no son los correctos", self.fila, self.columna)


    def mayor(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) > self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) > self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) > self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) > self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \">\" no son los correctos", self.fila, self.columna)


    def menor(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) < self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) < self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) < self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) < self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"<\" no son los correctos", self.fila, self.columna)


    def mayorIgual(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) >= self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) >= self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) >= self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) >= self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \">=\" no son los correctos", self.fila, self.columna)


    def menorIgual(self, opIzq, opDer):
        #boolean
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) <= self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) <= self.getType(self.opDer, opDer)
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) <= self.getType(self.opDer, opDer)
        elif (self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE) or (self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER):
            self.tipo = Tipo.BANDERA
            return self.getType(self.opIzq, opIzq) <= self.getType(self.opDer, opDer)
        return Excepcion("Semántico", "Los tipos de datos para el signo \"<=\" no son los correctos", self.fila, self.columna)


    def getType(self, nodo, valor):
        if nodo.tipo == Tipo.NUMBER:
            return int(valor)
        elif nodo.tipo == Tipo.DOBLE:
            return float(valor)
        elif nodo.tipo == Tipo.CADENA:
            return str(valor)
        elif nodo.tipo == Tipo.CARACTER:
            return str(valor)
        elif nodo.tipo == Tipo.BANDERA:
            if str(valor).lower() == 'true':
                return True
            elif str(valor).lower() == 'false':
                return False
        return valor

    def getNode(self):
        nodo = NodeCst("expresion")
        nodo.addChildNode(self.opIzq.getNode())
        nodo.addChild(str(self.tipoOperador(self.operador)))
        if self.opDer != None:
            nodo.addChildNode(self.opDer.getNode())
        return nodo


    def tipoOperador(self, op):
        if op == OperadorRelacional.MENOR:
            return '<'
        elif op == OperadorRelacional.MAYOR:
            return '>'
        elif op == OperadorRelacional.MENORIGUAL:
            return '<='
        elif op == OperadorRelacional.MAYORIGUAL:
            return '>='
        elif op == OperadorRelacional.IGUALIGUAL:
            return '=='
        elif op == OperadorRelacional.DIFERENTE:
            return '=!'