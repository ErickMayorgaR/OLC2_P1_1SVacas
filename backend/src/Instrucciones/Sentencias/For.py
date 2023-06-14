from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...Instrucciones.Sentencias.Break import Break
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo
from ...TS.TablaSimbolos import TablaSimbolos
from copy import copy

class If(Instruccion):
    def __init__(self, condicion, bloqueIf, bloqueElse, bloqueElseIf, fila, columna):
        self.condicion = condicion 
        self.bloqueIf = bloqueIf
        self.bloqueElse = bloqueElse
        self.bloqueElseIf = bloqueElseIf
        self.fila = fila
        self.columna = columna
        self.estado = False

    def interpretar(self, tree, table):
        self.estado = False #Bandera para saber si esta dentro del bloque if, else if o else
        
        condicion = self.condicion.interpretar(tree, table) #se evalua la condicion
        if isinstance(condicion, Excepcion): 
            return condicion

        if self.condicion.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control If", self.fila, self.columna)

        if condicion == True: #verifica si es verdadera la condicion
            for instruccion in self.bloqueIf:
                result = copy(instruccion).interpretar(tree, table)
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                if isinstance(result, Continue):
                    return result
                if isinstance(result, Return):
                    return result
                if isinstance(result, Break):
                    return result
            return True
        else: 
            #Verifica si hay un bloque Else if
            if self.bloqueElseIf != None: 
                for elseif in self.bloqueElseIf:
                    result = copy(elseif).interpretar(tree, table)

                    if isinstance(result, Excepcion):
                        return result
                    if isinstance(result, Continue):
                        return result
                    if isinstance(result, Return):
                        return result
                    if isinstance(result, Break):
                        return result
                    
                    if result == True:
                        self.estado = result #cambia el estado de la bandera para evitar que entre al bloque else
                        return None

            if self.bloqueElse != None and self.estado == False:
                for instruccion in self.bloqueElse:
                    result = copy(instruccion).interpretar(tree, table)
                    if isinstance(result, Excepcion):
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Continue):
                        return result
                    if isinstance(result, Return):
                        return result
                    if isinstance(result, Break):
                        return result         
                
    def getNode(self):
        nodo = NodeCst("if_instr")
        nodo.addChild("IF")
        nodo.addChildNode(self.condicion.getNode())

        instruccionesIfNodo = NodeCst("if_instr")
        for instruccion in self.instruccionesIf:
            instruccionesIfNodo.addChildNode(instruccion.getNode())
        nodo.addChildNode(instruccionesIfNodo)

        if self.instruccionesElse != None:
            instruccionesElseNodo = NodeCst("else_instr")
            for instruccion in self.instruccionesElse:
                instruccionesElseNodo.addChildNode(instruccion.getNode())
            nodo.addChildNode(instruccionesElseNodo)

        if self.ElseIf != None:
            instruccionesElseIfNodo = NodeCst("elseif_instr")
            for instruccion in self.ElseIf:
                instruccionesElseIfNodo.addChildNode(instruccion.getNode())
            nodo.addChildNode(instruccionesElseIfNodo)
        
        return nodo