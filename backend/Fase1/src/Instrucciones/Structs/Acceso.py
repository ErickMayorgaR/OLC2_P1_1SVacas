from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo

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

        structs = tree.getStructs()  # Obtener los structs de la tabla de símbolos
        tipo_simbolo = simbolo.getTipo()

        if not any(tipo_simbolo == struct.identificador for struct in structs):
            # Continuar la rutina si no se encuentra coincidencia
            return Excepcion("Semántico", f"La variable \"{self.identificador}\" a la que intenta acceder no es de tipo struct", self.fila, self.columna)

        try:
            valor = self.buscar_identificador(simbolo, self.atributo)
            if isinstance(valor, Excepcion):
                return valor
            if isinstance(valor, Excepcion):
                return valor
        except:
            return Excepcion("Semántico", "Atributo \""+self.atributo+"\" en variable \""+self.identificador+"\" no existe", self.fila, self.columna)

        self.tipo = simbolo.getValor().tabla[str(self.atributo)].tipo
        return valor

    def buscar_identificador(self, simbolo, identificador):
        valor = simbolo.getValor().tabla
        if isinstance(valor, dict):
            if identificador in valor:
                tipo = valor[identificador].tipo
                valor = valor[identificador].valor
                return tipo, valor
        elif isinstance(valor, list):
            for elemento in valor:
                if isinstance(elemento, Simbolo):
                    tipo, resultado = self.buscar_identificador(elemento, identificador)
                    if isinstance(resultado, Excepcion):
                        return resultado
                    elif resultado is not None:
                        return tipo, resultado
        return None, None


    def getNode(self):
        nodo = NodeCst("acceso_struct")
        nodoID = NodeCst("ID")
        nodoID.addChild(str(self.identificador))
        nodoAtributo = NodeCst("ID")
        nodoAtributo.addChild(str(self.atributo))
        nodo.addChildNode(nodoID)
        nodo.addChildNode(nodoAtributo)
        return nodo