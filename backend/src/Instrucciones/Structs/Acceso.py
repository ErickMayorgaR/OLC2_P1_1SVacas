from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo

class AccesoStruct(Instruccion):
    def __init__(self, identificador, atributo, fila, columna):
        self.identificador = identificador
        self.atributo = atributo
        self.fila = fila
        self.columna = columna
        self.tipo = 'any'

    def interpretar(self, tree, table):
        simbolo = table.getTabla(str(self.identificador))
        if simbolo == None:
            return Excepcion("Semántico", "Variable \""+self.identificador+"\" no encontrado", self.fila, self.columna)

        if simbolo.getTipo() != 'interface':
            return Excepcion("Semántico", "La varible \""+str(self.identificador)+"\" a la que intenta acceder no es tipo struct", self.fila, self.columna)

        try:
            valor =  simbolo.getValor().tabla[str(self.atributo)].valor
            if isinstance(valor, Excepcion):
                return valor
        except:
            return Excepcion("Semántico", "Atributo \""+self.atributo+"\" en variable \""+self.identificador+"\" no existe", self.fila, self.columna)

        self.tipo = simbolo.getValor().tabla[str(self.atributo)].tipo
        return valor

    def getNode(self):
        nodo = NodeCst("acceso_struct")
        nodoID = NodeCst("ID")
        nodoID.addChild(str(self.identificador))
        nodoAtributo = NodeCst("ID")
        nodoAtributo.addChild(str(self.atributo))
        nodo.addChildNode(nodoID)
        nodo.addChildNode(nodoAtributo)
        return nodo