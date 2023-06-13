from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Tipo import Tipo

class ModificacionStruct(Instruccion):
    def __init__(self, identificador, atributo, valor, fila, columna):
        self.identificador = identificador
        self.atributo = atributo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO

    def interpretar(self, tree, table):
        simbolo = table.getTabla(str(self.identificador)) #Encuentra la variable tipo strict

        if simbolo == None: #Ve si existe la variable existe
            return Excepcion("Semántico", "Variable \""+self.identificador+"\" no encontrado", self.fila, self.columna)

        if simbolo.getTipo() != Tipo.STRUCT: #Ve si la variable es tipo struct 
            return Excepcion("Semántico", "La varible \""+str(self.identificador)+"\" a la que intenta acceder no es tipo struct", self.fila, self.columna)

        struct = tree.getStruct(str(simbolo.getValor().owner)) #Busca el struct para sacar info jsjs
        if not(struct.mutable): #Verifica si la struct es mutable
            return Excepcion("Semántico", "La varible \""+str(self.identificador)+"\" es de tipo struct no mutable", self.fila, self.columna)
        
        try: #Verifica si existe ese parametro en el diccionario de los atributos jsjs
            simboloAtributo =  simbolo.getValor().tabla[str(self.atributo)]
            if isinstance(simboloAtributo, Excepcion):
                return simboloAtributo
        except:
            return Excepcion("Semántico", "Atributo \""+self.atributo+"\" en variable \""+self.identificador+"\" no existe", self.fila, self.columna)

        if not(self.verificarTipos(struct.atributos)): #Verifica si los tipos a asignar son los mismos
            return Excepcion("Semántico", "El valor a asignarse a atributo \""+self.atributo+"\" no es del mismo tipo", self.fila, self.columna)

        valor = self.valor.interpretar(tree, table)
        if isinstance(valor, Excepcion):
            return valor
        
        simboloAtributo.setValor(valor) #Actualiza el valor
        simboloAtributo.setTipo(self.valor.tipo)

        simbolo.getValor().tabla[str(self.atributo)] = simboloAtributo #Ya lo modifica en el atributo
        self.tipo = self.valor.tipo
        return None



    def verificarTipos(self, atributos):
        for atributo in atributos:
            if atributo['identificador'] == self.atributo:
                if atributo['tipo'] == self.valor.tipo or atributo['tipo'] == None:
                    return  True
                else:
                    return False

    def getNode(self):
        nodo = NodeCst("modificacion_struct")
        nodoID = NodeCst("ID")
        nodoID.addChild(str(self.identificador))
        nodoAtributo = NodeCst("ID")
        nodoAtributo.addChild(str(self.atributo))
        nodo.addChildNode(nodoID)
        nodo.addChildNode(nodoAtributo)
        nodo.addChildNode(self.valor.getNode())
        return nodo