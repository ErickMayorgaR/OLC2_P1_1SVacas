from ...Abstract.abstract import  Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Tipo import Tipo


class AsignacionVar(Instruccion):
    def __init__(self, identificador, valor, tipo, fila, columna):
        self.identificador = identificador
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        flag = False
        value = self.valor.interpretar(tree, table) #Interpreta el valor
        if isinstance(value, Excepcion):
            return value

        if self.tipo == 'any': #Ve si el tipo 
            self.tipo = self.valor.tipo 
        if self.tipo != None:
            if self.tipo != self.valor.tipo: #Verifica que el tipo asignado sea el mismo que el del valor
                return Excepcion("Semántico", "El tipo de dato en la variable \""+self.identificador+"\" es diferente", self.fila, self.columna)

        simboloVar = table.getTabla(str(self.identificador)) #Verifica si la variable ya existe en algún entorno
        

        if simboloVar != None:
                tablaSimbolo = table.getRealTabla(str(self.identificador))
                ambitoPadreFuncion =  table.getNombreTabla()
                #Por si se quiere declarar una variable igual en un entorno de funcion que ya exista en la global 
                if table.owner == 'function' and tablaSimbolo.owner == 'global':                                            
                    simboloVar = None
                elif tablaSimbolo.owner == 'global' and ambitoPadreFuncion == True:
                    simboloVar = None
            
                simbolo = Simbolo(str(self.identificador), simboloVar.tipo, value, self.fila, self.columna)
                result = table.actualizarTabla(simbolo)
                if isinstance(result, Excepcion):
                    return result
        elif simboloVar == None and flag == False:
            # La variable no fue encontrada en la tabla de símbolos, buscar en los parámetros de los structs
            structs = tree.getStructs()  # Obtener los structs de la tabla de símbolos

            for struct in structs:
                atributos = struct.atributos
                for atributo in atributos:
                    if atributo['identificador'] == self.identificador:
                        # La variable fue encontrada en los atributos de un struct
                        simbolo = Simbolo(str(self.identificador), atributo['tipo'], value, self.fila, self.columna)
                        result = table.setTabla(simbolo)
                        if isinstance(result, Excepcion):
                            return result
                        return None  # Terminar la búsqueda después de encontrar la variable en un struct
            flag = True

        elif simboloVar == None and flag == True: #Declara una variable
            simbolo = Simbolo(str(self.identificador), self.tipo, value, self.fila, self.columna)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion):
                return result
            

    def getNode(self):
        nodo = NodeCst("asignacion_instr")
        nodo.addChild(str(self.identificador))
        if self.tipo != None:
            nodo.addChild(str(self.tipoDato(self.tipo)))
        if self.valor != None:
            nodo.addChildNode(self.valor.getNode())
        return nodo

    def tipoDato(self, tipo):
        if tipo == 'booleano':
            return "Bool"
        elif tipo == 'string':
            return "String"
        elif tipo == 'number':
            return "Number"
        elif tipo == 'any':
            return "Anything"






