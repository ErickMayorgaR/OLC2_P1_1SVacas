from ..Instrucciones.Funcion.Funcion import Funcion
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import Tipo

class Upper(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo =  "any"

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador)

        if simbolo == None:
            return Excepcion("Semántico", "No se encontro el parametro de la funcion nativa \"Uppercase\"", self.fila, self.columna)

        if simbolo.getTipo() != 'string':
            return Excepcion("Semántico", "La variable \""+ self.identificador +"\" para Uppercase no es tipo number", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        return simbolo.getValor().upper()

    def getNode(self):
        nodo = NodeCst("nativas_instr")

        nodo.addChild(str(self.identificador))
        parametrosNodo = NodeCst("parametros")
        for parametro in self.parametros:
            parametroNodo = NodeCst("parametro")
            parametroNodo.addChild(str(self.tipoDato(parametro['tipo'])))
            idNodo = NodeCst("expresion")
            idNodo.addChild(str(parametro['identificador']))
            parametroNodo.addChildNode(idNodo)
            parametrosNodo.addChildNode(parametroNodo)
        nodo.addChildNode(parametrosNodo)

        instruccionesNodo = NodeCst("instrucciones")
        for instruccion in self.instrucciones:
            instruccionesNodo.addChildNode(instruccion.getNode())
        nodo.addChildNode(instruccionesNodo)

        return nodo