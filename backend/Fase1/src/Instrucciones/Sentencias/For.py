from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...Instrucciones.Sentencias.Break import Break
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...TS.Excepcion import Excepcion
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Simbolo import Simbolo
import src.Instrucciones.globals as globals
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
        nuevaTabla = TablaSimbolos('fordeclaration', table)
        globals.FlagFor = True

        # Si la declaracion no es nula, se ejecuta
        if self.declaracion != None:
            declaracion = self.declaracion.interpretar(tree, nuevaTabla)
            Identificador = self.declaracion.identificador 
            if isinstance(declaracion, Excepcion):
                tree.getExcepciones().append(declaracion)
                tree.updateConsola(declaracion.toString())
                return declaracion

        if isinstance(self.condicion, list):
            condicion = copy(self.condicion)
            self.copiarArreglo(condicion, self.condicion)
            val = self.interpretarArreglos(tree, nuevaTabla, condicion)
            if isinstance(val, Excepcion):
                globals.FlagFor = False
                tree.getExcepciones().append(condicion)
                tree.updateConsola(condicion.toString())
                return val
            condicionTipo = 'array'
        else:
            condicion = self.condicion.interpretar(tree, nuevaTabla)
            if isinstance(condicion, Excepcion):
                globals.FlagFor = False
                tree.getExcepciones().append(condicion)
                tree.updateConsola(condicion.toString())
                return condicion
            condicionTipo = self.condicion.tipo  
            
            if self.actualizacion != None:
                if self.condicion.tipo != 'boolean':
                    return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control For", self.fila, self.columna)
        
        if condicionTipo == 'string' or condicionTipo == 'array':  #Para cadenas
            for iterador in condicion:
                simbolo = Simbolo(str(Identificador), self.tipoDato(iterador), iterador, self.fila, self.columna)
                nuevaTabla.actualizarTabla(simbolo)
                nuevaTabla = TablaSimbolos('for', nuevaTabla)
                for instruccion in self.instrucciones:
                    result = instruccion.interpretar(tree, nuevaTabla)

                    if isinstance(result, Excepcion):
                        tree.getExcepciones().append(result)
                        tree.updateConsolaln(result.toString())
                        
                    if isinstance(result, Return): #Sentencia Return  
                        globals.FlagFor = False
                        return result.expresion
                        
                    if isinstance(result, Break): #Sentencia Break
                        globals.FlagFor = False
                        return None

                    if isinstance(result, Continue):
                        globals.FlagFor = False
                        break
            
        else:
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
        
                simbolo = Simbolo(self.declaracion.identificador, self.declaracion.tipo, nuevoValor, self.fila, self.columna)
                # Actualizando el valor de la variable en la tabla de simbolos
                valor = nuevaTabla.actualizarTabla(simbolo)
                if isinstance(valor, Excepcion): return valor


                condicion = self.condicion.interpretar(tree, nuevaTabla)
                if isinstance(condicion, Excepcion):
                    tree.getExcepciones().append(condicion)
                    tree.updateConsola(condicion.toString())
                    return condicion
                    
                if self.condicion.tipo != 'boolean':
                    return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control For", self.fila, self.columna)
        return None

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

    def tipoDato(self, value):
        if isinstance(value, int):
            return 'number'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, list):
            return 'array'

    def getNode(self):
        nodo = NodeCst("for_instr")
        nodo.addChild("FOR")
        nodo.addChild(self.declaracion.getNode())
        if isinstance(self.condicion, list):
            for izq in self.condicion:
                nodo.addChildNode(izq.getNode())
        else:
            nodo.addChildNode(self.condicion.getNode())
        if self.actualizacion != None:
            nodo.addChildNode(self.actualizacion.getNode())

        instruccionesNodo = NodeCst("instrucciones")
        for instruccion in self.instrucciones:
            instruccionesNodo.addChildNode(instruccion.getNode())
        nodo.addChildNode(instruccionesNodo)

        return nodo