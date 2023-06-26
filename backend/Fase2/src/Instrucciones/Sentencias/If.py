from ...Instrucciones.Funcion.LlamadaFuncion import LlamadaFuncion
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...Instrucciones.Sentencias.Break import Break
from ...Abstract.abstract import Instruccion
from ...TS.Excepcion import Excepcion
from ...TS.Tipo import Tipo

class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.ElseIf = ElseIf
        self.fila = fila
        self.columna = columna
        self.BREAK = ''
        self.CONTINUE = ''
        self.RETURN = ''


    def interpretar(self, tree, table, generator, etiqueta=None):
        ifOriginal = False
        if etiqueta == None:
            newLabel = generator.createLabel()
            etiqueta = newLabel
            ifOriginal = True

        condicion = self.condicion.interpretar(tree, table, generator)
        if isinstance(condicion, Excepcion):
            return condicion

        if self.condicion.tipo != Tipo.BANDERA:
            return Excepcion("Semántico", "Tipo de dato no bool en sentencia de control If", self.fila, self.columna)

        tree.updateConsola(generator.newLabel(condicion.trueLabel))

        for instruccion in self.instruccionesIf:
            if isinstance(instruccion, Continue):
                instruccion.label = self.CONTINUE
            if isinstance(instruccion, Break):
                instruccion.label = self.BREAK
            if isinstance(instruccion, Return):
                instruccion.label = self.RETURN
            
            resultIf = instruccion.interpretar(tree, table, generator)
            if isinstance(resultIf, Excepcion):
                return resultIf
            if isinstance(resultIf, Return):
                if generator.LabelReturn == '':
                    generator.LabelReturn = generator.createLabel()
                
                tree.updateConsola(generator.newGoto(generator.LabelReturn))


        tree.updateConsola(generator.newGoto(etiqueta))
        tree.updateConsola(generator.newLabel(condicion.falseLabel))

        if self.ElseIf:
            for elseIf in self.ElseIf:
                resultElseIf = elseIf.interpretar(tree, table, generator, etiqueta)
                if isinstance(resultElseIf, Excepcion):
                    return resultElseIf
                if isinstance(resultElseIf, Continue):
                    return resultElseIf
                if isinstance(resultElseIf, Return):
                    if generator.LabelReturn == '':
                        generator.LabelReturn = generator.createLabel()
                
                    tree.updateConsola(generator.newGoto(generator.LabelReturn))
                if isinstance(resultElseIf, Break):
                    return resultElseIf 

        if self.instruccionesElse:
            for elsee in self.instruccionesElse:
                resultElse = elsee.interpretar(tree, table, generator)
                if isinstance(resultElse, Excepcion):
                    return resultElse
                if isinstance(resultElse, Continue):
                    return resultElse
                if isinstance(resultElse, Return):
                    if generator.LabelReturn == '':
                        generator.LabelReturn = generator.createLabel()
                
                        tree.updateConsola(generator.newGoto(generator.LabelReturn))
                if isinstance(resultElse, Break):
                    return resultElse
            tree.updateConsola(generator.newGoto(etiqueta))

        if ifOriginal:
            tree.updateConsola(generator.newLabel(etiqueta))


    def getNode(self):
        return super().getNode()