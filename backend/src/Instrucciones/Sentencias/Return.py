from ...Abstract.abstract import Instruccion
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo


class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = 'any'
        self.result = None

    def interpretar(self, tree, table):
        if self.expresion == None:
            self.result = 'Nothing'
            return self
        
        if isinstance(self.expresion, list):
            resultados = []
            for expresion in self.expresion:
                result = expresion.interpretar(tree, table)
                if isinstance(result, Excepcion):
                    return result
                resultados.append(result)
            self.tipo = 'interface' #se le asigna el tipo a la expresion de return 
            self.result = resultados
        else:
            result = self.expresion.interpretar(tree, table)    
            if isinstance(result, Excepcion):
                return result
            self.tipo = self.expresion.tipo #se le asigna el tipo a la expresion de return 
            self.result = result


        return self #Retorna el mismo nodo para poder acceder a sus atributos

    def getNode(self):
        nodo = NodeCst("return_instr")
        nodo.addChild("RETURN")
        nodo.addChildNode(self.expresion.getNode())
        return nodo