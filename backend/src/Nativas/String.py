from ..Abstract.abstract import Instruccion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import Tipo

class String(Instruccion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.instrucciones = instrucciones
        self.tipo = "string"

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)
        if simbolo == None: return Excepcion("Semantico", "No se encontro el parametro de toString", self.fila, self.columna)
        simbolo.setTipo("string")
        return str(simbolo.getValor())
        
        
    def getNode(self):
        nodo = NodeCst("nativas_instr")
        nodo.addChild("STRING")
        nodo.addChildNode(self.expresion.getNode())
        return nodo