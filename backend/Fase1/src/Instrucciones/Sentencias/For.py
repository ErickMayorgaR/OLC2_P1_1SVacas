from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...Instrucciones.Sentencias.Break import Break
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Simbolo import Simbolo
from copy import copy

class For(Instruccion):
    def __init__(self, declaracion, condicion, actualizacion, instrucciones, fila, columna):
        self.declaracion = declaracion
        self.condicion = condicion
        self.actualizacion = actualizacion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table) #NUEVO ENTORNO

        # Si la declaracion no es nula, se ejecuta
        if self.declaracion != None:
            declaracion = self.declaracion.interpretar(tree, nuevaTabla)
            if isinstance(declaracion, Excepcion):
                tree.getExcepciones().append(declaracion)
                tree.updateConsola(declaracion.toString())
                return declaracion
            
        condicion = self.condicion.interpretar(tree, nuevaTabla)
        if isinstance(condicion, Excepcion):
            tree.getExcepciones().append(condicion)
            tree.updateConsola(condicion.toString())
            return condicion
            
        if self.condicion.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control For", self.fila, self.columna)
        
        while condicion:
            for instruccion in self.instrucciones:
                result = copy(instruccion).interpretar(tree, nuevaTabla)
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                if isinstance(result, Continue):
                    break
                if isinstance(result, Return):
                    return result
                if isinstance(result, Break):
                    return None
                
            
            nuevoValor = self.actualizacion.interpretar(tree, nuevaTabla)
            if isinstance(nuevoValor, Excepcion):
                tree.getExcepciones().append(nuevoValor)
                tree.updateConsola(nuevoValor.toString())
                return nuevoValor
      
            simbolo = Simbolo(self.declaracion.identificador, self.tipo,  self.fila, self.columna)
            # Actualizando el valor de la variable en la tabla de simbolos
            valor = nuevaTabla.actualizarTabla(simbolo)
            if isinstance(valor, Excepcion): return valor


            condicion = self.condicion.interpretar(tree, nuevaTabla)
            if isinstance(condicion, Excepcion):
                tree.getExcepciones().append(condicion)
                tree.updateConsola(condicion.toString())
                return condicion
                
            if self.condicion.tipo != Tipo.BANDERA:
                return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control For", self.fila, self.columna)
        return None

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