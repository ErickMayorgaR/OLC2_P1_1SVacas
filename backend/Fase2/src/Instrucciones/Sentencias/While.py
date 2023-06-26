from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...Instrucciones.Sentencias.Break import Break
from ...Expresiones.Aritmeticas.Suma import Suma
from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo
from ...Instrucciones.Sentencias.If import If

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table, generator):
        newLabel = generator.createLabel()
        tree.updateConsola(generator.newLabel(newLabel))

        condicion = self.condicion.interpretar(tree, table, generator)
        if isinstance(condicion, Excepcion):
            return condicion

        if self.condicion.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "La condición de While no es tipo boolean", self.fila, self.columna)

        tree.updateConsola(generator.newLabel(condicion.trueLabel))
        nuevaTabla = TablaSimbolos('while', table)

        for instruccion in self.instrucciones:
            if isinstance(instruccion, If):
                instruccion.BREAK = condicion.falseLabel
                instruccion.CONTINUE = newLabel
                instruccion.RETURN = condicion.falseLabel

            if isinstance(instruccion, Break):
                instruccion.label = condicion.falseLabel
            if isinstance(instruccion, Continue):
                instruccion.label = newLabel
            if isinstance(instruccion, Return):
                instruccion.label = condicion.falseLabel
            
            result = instruccion.interpretar(tree, nuevaTabla, generator)
            if isinstance(result, Excepcion):
                tree.getExcepciones().append(result)
                tree.updateConsolaln(result.toString())

        tree.updateConsola(generator.newGoto(newLabel))
        tree.updateConsola(generator.newLabel(condicion.falseLabel))

    def getNode(self):
        return super().getNode()