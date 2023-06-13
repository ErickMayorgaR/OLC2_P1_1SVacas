from ..Abstract.abstract import Instruccion
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import OperadorAritmetico, Tipo
from ..Abstract.NodeCst import NodeCst

class Aritmetica(Instruccion):

    def __init__(self, operador, opIzq, opDer, fila, columna):
        self.opIzq = opIzq 
        self.opDer = opDer 
        self.operador = operador
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

        #suma
        if self.operador == OperadorAritmetico.MAS:
            return self.suma(opIzq, opDer)

        #resta
        elif self.operador == OperadorAritmetico.MENOS:
            return self.resta(opIzq, opDer)

        #multiplicacion
        elif self.operador == OperadorAritmetico.ASTERISCO:
            return self.multiplicacion(opIzq, opDer)

        #division
        elif self.operador == OperadorAritmetico.DIVISION:
            if opDer != 0:
                return self.division(opIzq, opDer)
            else:
                return Excepcion("Semántico", "No se puede dividir entre cero", self.fila, self.columna) 
            
        #potencia
        elif self.operador == OperadorAritmetico.POTENCIA:
            return self.potencia(opIzq, opDer)
        
        #modulo
        elif self.operador == OperadorAritmetico.PORCENTAJE:
            if opDer != 0:
                return self.modulo(opIzq, opDer)
            else:
                return Excepcion("Semántico", "No se puede hacer mmodulo de cero", self.fila, self.columna) 

        #unario
        elif self.operador == OperadorAritmetico.UMENOS:
            return self.negativo(opIzq)

        return Excepcion("Semántico", "Tipo de Operacion no Especificado.", self.fila, self.columna)
        


    def suma(self, opIzq, opDer):
        #entero
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return int(self.getType(self.opIzq, opIzq) + self.getType(self.opDer, opDer))

        #decimal
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) + self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) + self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) + self.getType(self.opDer, opDer))

        return Excepcion("Semántico", "Los tipos de datos para el signo \"+\" no pueden ser operados", self.fila, self.columna)
    
    def resta(self, opIzq, opDer):
         #entero
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return int(self.getType(self.opIzq, opIzq) - self.getType(self.opDer, opDer))

        #decimal
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) - self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) - self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) - self.getType(self.opDer, opDer))

        return Excepcion("Semántico", "Los tipos de datos para el signo \"-\" no pueden ser operados", self.fila, self.columna)


    def multiplicacion(self, opIzq, opDer):
        #entero
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return int(self.getType(self.opIzq, opIzq) * self.getType(self.opDer, opDer))

        #decimal
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) * self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) * self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) * self.getType(self.opDer, opDer))

        #string
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.CADENA:
            self.tipo = Tipo.CADENA
            return str(self.getType(self.opIzq, opIzq) + self.getType(self.opDer, opDer))

        return Excepcion("Semántico", "Los tipos de datos para el signo \"*\" no pueden ser operados", self.fila, self.columna)


    def division(self, opIzq, opDer):
        #decimal
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) / self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) / self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) / self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) / self.getType(self.opDer, opDer))
    
        return Excepcion("Semántico", "Los tipos de datos para el signo \"\\\" no pueden ser operados", self.fila, self.columna)


    def potencia(self, opIzq, opDer):
        #entero
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return int(self.getType(self.opIzq, opIzq) ** self.getType(self.opDer, opDer))

        #decimal
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) ** self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) ** self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) ** self.getType(self.opDer, opDer))

        #cadena
        elif self.opIzq.tipo == Tipo.CADENA and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.CADENA
            return str(self.getType(self.opIzq, opIzq) * self.getType(self.opDer, opDer))

        return Excepcion("Semántico", "Los tipos de datos para el signo \"^\" no pueden ser operados", self.fila, self.columna)


    def modulo(self, opIzq, opDer):
        #entero
        if self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.NUMBER
            return int(self.getType(self.opIzq, opIzq) % self.getType(self.opDer, opDer))

        #decimal
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.NUMBER:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) % self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.NUMBER and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) % self.getType(self.opDer, opDer))
        elif self.opIzq.tipo == Tipo.DOBLE and self.opDer.tipo == Tipo.DOBLE:
            self.tipo = Tipo.DOBLE
            return float(self.getType(self.opIzq, opIzq) % self.getType(self.opDer, opDer))

        return Excepcion("Semántico", "Los tipos de datos para el signo \"%\" no pueden ser operados", self.fila, self.columna)


    def negativo(self, opIzq):
        if self.operador == OperadorAritmetico.UMENOS:
            #Entero
            if self.opIzq.tipo == Tipo.NUMBER:
                self.tipo = Tipo.NUMBER
                return -self.getType(self.opIzq, opIzq)
            #Decimal
            elif self.opIzq.tipo == Tipo.DOBLE:
                self.tipo = Tipo.DOBLE
                return -self.getType(self.opIzq, opIzq)
        return Excepcion("Semántico", "Tipo Erroneo de operacion para - unario.", self.fila, self.columna)


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
        if op == OperadorAritmetico.MAS:
            return '+'
        elif op == OperadorAritmetico.MENOS:
            return '-'
        elif op == OperadorAritmetico.ASTERISCO:
            return '*'
        elif op == OperadorAritmetico.DIVISION:
            return '/'
        elif op == OperadorAritmetico.PORCENTAJE:
            return '%'
        elif op == OperadorAritmetico.POTENCIA:
            return '^'
        elif op == OperadorAritmetico.UMENOS:
            return '-'