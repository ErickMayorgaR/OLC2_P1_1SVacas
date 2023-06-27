from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion
from ..Expresiones.primitivos import Primitivos

class String(Instruccion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.instrucciones = instrucciones
        self.value = None
        self.tipo = "string"

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None: return Excepcion("Semantico", "No se encontro el parametro de toString", self.fila, self.columna)
        simbolo.setTipo("string")
        self.value = Primitivos(simbolo.identificador, simbolo.valor, simbolo.fila,simbolo.columna)
        return str(simbolo.getValor())
        
        
    def getNode(self):
        nodo = NodeCst("nativas_instr")
        nodo.addChild("STRING")
        nodo.addChildNode(self.value.getNode())
        return nodo