from ..Abstract.abstract import Instruccion
from ..TS.TablaSimbolos import TablaSimbolos
from ..Abstract.NodeCst import NodeCst
from ..TS.Excepcion import Excepcion
from ..TS.Tipo import Tipo
from copy import copy

class Imprimir(Instruccion):
    def __init__(self, expresiones, saltoLinea, fila, columna):
        self.expresiones = expresiones
        self.saltoLinea = saltoLinea
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        valores = ""
        valor = ""
        if self.expresiones != None:
            for expresion in self.expresiones:
                valor = expresion.interpretar(tree, table) #Retorna cualquier valor interpretado
                if isinstance(valor, Excepcion):
                    return valor
                valores += str(valor)
        elif self.expresiones == None and self.saltoLinea == True:
            valores = "\n"
                
        if isinstance(valor, TablaSimbolos):
            nuevoValor = copy(valor.tabla)
            self.interpretarStruct(nuevoValor, valor.tabla)
            valores = str(nuevoValor)

        if(self.saltoLinea == True):
            tree.updateConsolaln(valores)
        else:
            tree.updateConsola(valores)
        return None

    def interpretarStruct(self, structNuevo, struct):
        for keys, value in struct.items(): 
            structNuevo[keys] = value.valor
            if isinstance(value.valor, TablaSimbolos):
                structNuevo[keys] = copy(value.valor.tabla)
                self.interpretarStruct(structNuevo[keys],value.valor.tabla)
        return None
    
    def getNode(self):
        nodo = NodeCst("ConsoleLog")
        if isinstance(self.expresiones, list):
            for expresion in self.expresiones:
                nodo.addChildNode(expresion.getNode())
        elif self.expresiones == None:
            nodo.addChild("")    
        else:
            nodo.addChildNode(self.expresiones.getNode())    
        return nodo