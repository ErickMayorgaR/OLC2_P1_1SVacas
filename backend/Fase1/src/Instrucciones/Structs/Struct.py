from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo

class Struct(Instruccion):
    def __init__(self, identificador, atributos, fila, columna):
        self.identificador = identificador
        self.atributos = atributos
        self.tipo = 'interface'
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNode(self):
        nodo = NodeCst("structs_instr")
        nodo.addChild("STRUCT")
        nodo.addChild(str(self.identificador))
        atributosNodo = NodeCst("lista_atributos")
        for atributo in self.atributos:
            atributoNodo = NodeCst("atributo")
            atributoNodo.addChild(str(self.tipoDato(atributo['tipo'])))
            idNodo = NodeCst("ID")
            idNodo.addChild(str(atributo['identificador']))
            atributoNodo.addChildNode(idNodo)
            atributosNodo.addChildNode(atributoNodo)
        nodo.addChildNode(atributosNodo)
        return nodo

    def tipoDato(self, tipo):
        if tipo == 'boolean':
            return "Bool"
        elif tipo == 'string':
            return "String"
        elif tipo == 'number':
            return "Number"
        elif tipo == 'any':
            return "Anything"
