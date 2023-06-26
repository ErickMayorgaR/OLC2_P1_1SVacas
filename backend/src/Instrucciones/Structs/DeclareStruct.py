
from ...Abstract.abstract import Instruccion
from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...Abstract.NodeCst import NodeCst
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo

class DeclareStruct(Instruccion):
    def __init__(self, identificador, ide_struct, parametros, fila, columna):
        self.identificador = identificador
        self.identificador_struct = ide_struct
        self.parametros = parametros
        self.fila = fila
        self.columna  = columna

    def interpretar(self, tree, table):
        struct = tree.getStruct(str(self.identificador_struct))

        if self.identificador == None:
            self.identificador = self.identificador_struct

        if struct != None: #Para las structs
            nuevaTabla = TablaSimbolos(str(self.identificador_struct), table)
            
            if len(struct.atributos) != len(self.parametros):
                return Excepcion("Semántico", "Cantidad de parámetros incorrecta para struct \""+self.identificador+"\"", self.fila, self.columna)

            simbolo = Simbolo(self.identificador, self.identificador_struct, None, self.fila, self.columna)
            resultTable = table.setTabla(simbolo)
            
            if isinstance(resultTable, Excepcion):
                return resultTable
            
            for atributo in struct.atributos:
                if any(parametro['identificador'] == atributo['identificador'] for parametro in self.parametros):
                    indice = next((i for i, p in enumerate(self.parametros) if p['identificador'] == atributo['identificador']), None)
                    if indice is not None:
                        expresion = self.parametros[indice]['parametro']
                        if isinstance(expresion, list):
                            result_final = []
                            for expr in expresion:
                                resultExpresion = expr['parametro'].interpretar(tree, table)
                                tipo = expr['parametro'].tipo
                                if isinstance(resultExpresion, Excepcion):
                                    return resultExpresion
                                simbolo = Simbolo(expr['identificador'], tipo, resultExpresion, self.fila, self.columna)
                                result_final.append(simbolo)
                                
                            simbolo_result = Simbolo(atributo['identificador'], atributo['tipo'], result_final, self.fila, self.columna)
                            resultTable = nuevaTabla.setTabla(simbolo_result)
                            if isinstance(resultTable, Excepcion):
                                return resultTable
                        else:
                            resultExpresion = expresion['parametro'].interpretar(tree, table)
                            tipo = expr['parametro'].tipo
                            if isinstance(resultExpresion, Excepcion):
                                return resultExpresion
                            simbolo_result = Simbolo(atributo['identificador'], atributo['tipo'], resultExpresion, self.fila, self.columna)
                            resultTable = nuevaTabla.setTabla(simbolo_result)
                            if isinstance(resultTable, Excepcion):
                                return resultTable
                    else:
                        return Excepcion("Semántico", "El atributo \""+atributo['identificador']+"\" no se encuentra definido en el struct \""+self.identificador+"\"", self.fila, self.columna)

            
            self.tipo = struct.tipo
            valor = struct.interpretar(tree, nuevaTabla)
            if isinstance(valor, Excepcion):
                return valor
            return nuevaTabla
        else:
            return Excepcion("Semántico", "Struct \""+self.identificador_struct+"\" no encontrado", self.fila, self.columna)


        
    def getNode(self):
        nodo = NodeCst("llamada_funcion_instr")
        nodo.addChild(str(self.identificador))
        
        parametrosNodo = NodeCst("parametros_llamada")
        for parametro in self.parametros:
            parametroNodo = NodeCst("parametro_llamada")
            parametroNodo.addChild(parametro.getNode())
            parametrosNodo.addChildNode(parametroNodo)

        nodo.addChildNode(parametrosNodo)
        
        return nodo