from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...Instrucciones.Sentencias.Break import Break
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo
from ...TS.TablaSimbolos import TablaSimbolos

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.condicion = condicion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion):
                return condicion
            if self.condicion.tipo == Tipo.BANDERA:
                if condicion == True: #Verifica en cada ciclo que la condicion sea verdadera
                    nuevaTabla = TablaSimbolos('while', table) #Se crea un nuevo entorno 
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)
                        
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsolaln(result.toString())
                        
                        if isinstance(result, Return): #Sentencia Return  
                            return result
                        
                        if isinstance(result, Break): #Sentencia Break
                            return None

                        if isinstance(result, Continue):
                            break

                elif condicion == False:
                    break
            else:
                return Excepcion("Semántico", "La condición de While no es tipo boolean", self.fila, self.columna)

    def getNode(self):
        nodo = NodeCst("while_instr")
        nodo.addChild("WHILE")
        nodo.addChildNode(self.condicion.getNode())
        
        instruccionesNodo = NodeCst("instrucciones")
        for instruccion in self.instrucciones:
            instruccionesNodo.addChildNode(instruccion.getNode())
        nodo.addChildNode(instruccionesNodo)

        return nodo
        