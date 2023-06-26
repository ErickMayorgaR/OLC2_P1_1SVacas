from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...Instrucciones.Sentencias.Break import Break
from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Valor import Value
from ...TS.Tipo import Tipo

class Funcion(Instruccion):
    def __init__(self, identificador, parametros, tipo, instrucciones, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.size = 0
        self.tipo = tipo
        self.primerTemp = 0
        self.Temporales = {}

    def interpretar(self, tree, table, generator):
        print(generator.temporal)
        nuevaTabla = TablaSimbolos('function', table)
        self.primerTemp = generator.temporal
        
        tamanoTabla = nuevaTabla.size  #Guardando el valor del tamano de todos los entornos
        nuevaTabla.changeOwnSize(1)    #Sumandole 1 del return 
        nuevaTabla.size = nuevaTabla.ownSize  #Asignandole cero a la nueva tabla pq asi la funcion empieza de cero  
        
        tree.updateConsolaln("\nfunc " + self.identificador + "(){")

        for parametro in self.parametros:
            tamTabla = nuevaTabla.size #Tamano de tabla jeje
            #Creacion de simbolo e ingresandolo a la tabla de simbolos
            value = self.returnValueType(parametro['tipo']) #Solo poniendo un valor aleatorio para ver si cumple con los requisitos
            simbolo = Simbolo(parametro['identificador'], parametro['tipo'], value, tamTabla, False, False, self.fila, self.columna)
            resultTable = nuevaTabla.setTabla(simbolo)
            if isinstance(resultTable, Excepcion):
                return resultTable

        for instruccion in self.instrucciones:
            value = instruccion.interpretar(tree, nuevaTabla, generator) #Devuelve el nodo del resultado de la funcion si es un return
            if isinstance(value, Excepcion):
                tree.getExcepciones().append(value)
                tree.updateConsolaln(value.toString())
            if isinstance(value, Continue):
                err = Excepcion("Semántico", "Sentencia CONTUNUE fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsolaln(err.toString())
            if isinstance(value, Break):
                err = Excepcion("Semántico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsolaln(err.toString())
            if isinstance(value, Return):
                if generator.LabelReturn == '':
                    generator.LabelReturn = generator.createLabel()
                
                tree.updateConsola(generator.newGoto(generator.LabelReturn))
                self.tipo = value.tipo

        if generator.LabelReturn != '':
            tree.updateConsola(generator.newLabel(generator.LabelReturn))
            
        tree.updateConsola(generator.newReturn())
        tree.updateConsolaln("}")

        nuevaTabla.size = tamanoTabla #Regresando el valor de la tabla a su valor actual
        print(generator.temporal-1)
        return None

    def getNode(self):
        return super().getNode()

    def returnValueType(self, tipo):
        if tipo == Tipo.NUMBER:
            return Value(1, '', tipo, False)
        elif tipo == Tipo.BANDERA:
            return Value(True, '', tipo, False)
        elif tipo == Tipo.CADENA:
            return Value('', '', tipo, False)