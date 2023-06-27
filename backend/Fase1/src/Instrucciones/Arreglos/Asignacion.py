from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo 
from copy import copy

class AsignacionArreglos(Instruccion):
    def __init__(self, identificador, expresiones, tipo, fila, columna):
        self.identificador = identificador 
        self.expresiones = expresiones
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.value = ""

    def interpretar(self, tree, table):
        value = copy(self.expresiones)
        self.copiarArreglo(value, self.expresiones)
        val = self.interpretarArreglos(tree, table, value)
        if isinstance(val, Excepcion):
            return val
        self.value = value
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


    def interpretarArreglos(self, tree, table, arreglo):
        i = 0
        while i < len(arreglo):
            if isinstance(arreglo[i], list):
                self.interpretarArreglos(tree, table, arreglo[i])
            else:
                valor = arreglo[i].interpretar(tree, table)
                if isinstance(valor, Excepcion):
                    return valor
                arreglo[i] = valor
            i += 1
        return None
                  
    def copiarArreglo(self, valor, arreglo):
        i = 0
        while i < len(arreglo):
            if isinstance(arreglo[i], list):
                valor[i] = copy(arreglo[i])
            else:
                valor[i] = copy(arreglo[i])
            i += 1
        return None 


    def getNode(self):
        nodo = NodeCst("asignacion_instr")
        nodo.addChild(str(self.identificador))
        expresionsNode = NodeCst("expresion")
        expresionsNode.addChild(str(self.value))
        nodo.addChildNode(expresionsNode)
        return nodo
