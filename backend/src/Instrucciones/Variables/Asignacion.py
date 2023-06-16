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
        self.globall = False

    def interpretar(self, tree, table):
        value = self.valor.interpretar(tree, table) #Interpreta el valor
        if isinstance(value, Excepcion):
            return value

        if self.tipo == None: #Ve si el tipo 
            self.tipo = self.valor.tipo 

        if Tipo[self.tipo.upper()] != self.valor.tipo: #Verifica que el tipo asignado sea el mismo que el del valor
            return Excepcion("Semántico", "El tipo de dato en la variable \""+self.identificador+"\" es diferente", self.fila, self.columna)

        simboloVar = table.getTabla(str(self.identificador)) #Verifica si la variable ya existe en algún entorno
        

        if simboloVar != None:
            if simboloVar.globall == False and  simboloVar.local == False:
                tablaSimbolo = table.getRealTabla(str(self.identificador))
                ambitoPadreFuncion =  table.getNombreTabla()
                #Por si se quiere declarar una variable igual en un entorno de funcion que ya exista en la global 
                if table.owner == 'function' and tablaSimbolo.owner == 'global':                                            
                    simboloVar = None
                elif tablaSimbolo.owner == 'global' and ambitoPadreFuncion == True:
                    simboloVar = None


        if simboloVar != None: #Reasigna una variable ya existente
            if simboloVar.globall: #Si la variable es global
                simbolo = Simbolo(str(self.identificador), self.tipo, value, False, True, self.fila, self.columna)
                result = table.actualizarTabla(simbolo) #Actualiza la variable del entorno global
                if isinstance(result, Excepcion):
                    return result
                resultGlobal = tree.getTSGlobal().actualizarTabla(simbolo) #Actualiza la variable global
                if isinstance(resultGlobal, Excepcion):
                    return result
            
            elif simboloVar.local: #Si la variable es local
                simbolo = Simbolo(str(self.identificador), self.tipo, value, True, False, self.fila, self.columna)
                result = table.actualizarTabla(simbolo) #Actualiza la variable local mas cercana
                if isinstance(result, Excepcion):
                    return result
            
            else: #Si se declara normalita
                simbolo = Simbolo(str(self.identificador), self.tipo, value, False, False, self.fila, self.columna)
                result = table.actualizarTabla(simbolo)
                if isinstance(result, Excepcion):
                    return result

        elif simboloVar == None: #Declara una variable
            simbolo = Simbolo(str(self.identificador), self.tipo, value, False, False, self.fila, self.columna)
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






