from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo

class Struct(Instruccion):
    def __init__(self, identificador, atributos, mutable, fila, columna):
        self.identificador = identificador
        self.atributos = atributos
        self.mutable = mutable
        self.tipo = Tipo.STRUCT
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNode(self):
        nodo = NodeCst("structs_instr")
        if self.mutable:
            nodoMutable = NodeCst("structs_mutable")
            nodoMutable.addChild("MUTABLE")
            nodoMutable.addChild("STRUCT")
            nodoMutable.addChild(str(self.identificador))
            atributosNodo = NodeCst("lista_atributos")
            for atributo in self.atributos:
                atributoNodo = NodeCst("atributo")
                atributoNodo.addChild(str(self.tipoDato(atributo['tipo'])))
                idNodo = NodeCst("ID")
                idNodo.addChild(str(atributo['identificador']))
                atributoNodo.addChildNode(idNodo)
                atributosNodo.addChildNode(atributoNodo)
            nodoMutable.addChildNode(atributosNodo)
            nodo.addChildNode(nodoMutable)
        else:
            nodoInmutable = NodeCst("structs_inmutable")
            nodoInmutable.addChild("STRUCT")
            nodoInmutable.addChild(str(self.identificador))
            atributosNodo = NodeCst("lista_atributos")
            for atributo in self.atributos:
                atributoNodo = NodeCst("atributo")
                atributoNodo.addChild(str(self.tipoDato(atributo['tipo'])))
                idNodo = NodeCst("ID")
                idNodo.addChild(str(atributo['identificador']))
                atributoNodo.addChildNode(idNodo)
                atributosNodo.addChildNode(atributoNodo)
            nodoInmutable.addChildNode(atributosNodo)
            nodo.addChildNode(nodoInmutable)
        return nodo

    def tipoDato(self, tipo):
        if tipo == Tipo.BANDERA:
            return "Bool"
        elif tipo == Tipo.CADENA:
            return "String"
        elif tipo == Tipo.CARACTER:
            return "Char"
        elif tipo == Tipo.DOBLE:
            return "Float64"
        elif tipo == Tipo.NUMBER:
            return "Int64"
        elif tipo == Tipo.NULO:
            return "Nothing"
