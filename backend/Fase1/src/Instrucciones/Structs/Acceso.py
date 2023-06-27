from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo

class AccesoStruct(Instruccion):
    def __init__(self, identificador, atributo1, atributo2, fila, columna):
        self.identificador = identificador
        self.atributo1 = atributo1
        self.atributo2 = atributo2
        self.fila = fila
        self.columna = columna
        self.tipo = 'any'

    def interpretar(self, tree, table):
        simbolo = table.getTabla(str(self.identificador))
        if simbolo == None:
            return Excepcion("Semántico", "Variable \""+self.identificador+"\" no encontrado", self.fila, self.columna)

        structs = tree.getStructs()  # Obtener los structs de la tabla de símbolos
        tipo_simbolo = simbolo.getTipo()

        if not any(tipo_simbolo == struct.identificador for struct in structs):
            # Continuar la rutina si no se encuentra coincidencia
            return Excepcion("Semántico", f"La variable \"{self.identificador}\" a la que intenta acceder no es de tipo struct", self.fila, self.columna)

        try:
            [tipo, valor] = self.buscar_identificador(simbolo, self.atributo1, self.atributo2)
            self.tipo = tipo
            if isinstance(valor, Excepcion):
                return valor
            if isinstance(valor, Excepcion):
                return valor
        except:
            return Excepcion("Semántico", "Atributo \""+self.atributo1+"\" en variable \""+self.identificador+"\" no existe", self.fila, self.columna)

        return valor

    def buscar_identificador(self, simbolo, identificador1, identificador2):
        valor = simbolo.getValor()
        if isinstance(valor, list):
            for elemento in valor:
                if elemento.identificador == identificador2:
                    if isinstance(elemento, list):
                        for atributo in elemento:
                            if atributo.identificador == identificador1:
                                tipo, resultado = self.buscar_identificador(atributo, None, elemento)
                                if isinstance(resultado, Excepcion):
                                    return resultado
                                elif resultado is not None:
                                    return tipo, resultado

                    elif isinstance(elemento, Simbolo):
                        tipo, resultado = self.buscar_identificador(elemento, None, identificador1)
                        if isinstance(resultado, Excepcion):
                            return resultado
                        elif resultado is not None:
                            return tipo, resultado
        else:
            tipo = simbolo.getTipo()
            return tipo, valor
        return None, None


    def getNode(self):
        nodo = NodeCst("acceso_struct")
        nodoID = NodeCst("ID")
        nodoID.addChild(str(self.identificador))
        nodoAtributo = NodeCst("ID")
        nodoAtributo.addChild(str(self.atributo1))
        nodo.addChildNode(nodoID)
        nodo.addChildNode(nodoAtributo)
        return nodo