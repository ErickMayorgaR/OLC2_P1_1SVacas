from ...Instrucciones.Variables.Declaracion import DeclaracionVar
from ...Instrucciones.Variables.Asignacion import AsignacionVar
from ...Expresiones.Relaciones.Diferente import Diferente
from ...Instrucciones.Sentencias.Continue import Continue
from ...Instrucciones.Sentencias.Return import Return
from ...Instrucciones.Sentencias.Break import Break
from ...Expresiones.Primitivos.Identificador import Identificador
from ...Expresiones.Primitivos.Negativo import Negativo
from ...Expresiones.Relaciones.MenorIgual import MenorIgual
from ...Expresiones.Primitivos.Number import Number
from ...Expresiones.Primitivos.Temp import Temporal
from ...Instrucciones.Sentencias.If import If
from ...Expresiones.Aritmeticas.Suma import Suma
from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Excepcion import Excepcion
from ...TS.Valor import Value
from ...TS.Tipo import Tipo



class For(Instruccion):
    def __init__(self, identificador, expresionIzq, expresionDer, instrucciones, extra, fila, columna):
        self.identificador = identificador
        self.expresionIzq = expresionIzq
        self.expresionDer = expresionDer
        self.instrucciones = instrucciones
        self.extra = extra
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table, generator):
        nuevaTablaIntermedia = TablaSimbolos('fordeclaration', table)

        if isinstance(self.expresionIzq, list):
            pass
        else:
            expIzq = self.expresionIzq.interpretar(tree, nuevaTablaIntermedia, generator)
            if isinstance(expIzq, Excepcion):
                return expIzq
            expresionIzqTipo = self.expresionIzq.tipo

        if expresionIzqTipo == Tipo.CADENA:
            #Declarando Contador
            IndiceCadena = Temporal(expIzq, self.fila, self.columna)            
            result = DeclaracionVar('contador', IndiceCadena, expresionIzqTipo, True, False, self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            if isinstance(result, Excepcion):
                return result

            
            #Declarando String para caracteres 
            IndiceCadena = Identificador('contador', self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            ValorCadena = generator.createTemp()
            tree.updateConsola(generator.newGetHeap(ValorCadena, IndiceCadena.getTemporal()))
            valor = Value('', ValorCadena, Tipo.CADENA, True)    
            ValorCadena = Temporal(valor, self.fila, self.columna)
            
            result = DeclaracionVar(self.identificador, ValorCadena, Tipo.CADENA, True, False, self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            if isinstance(result, Excepcion):
                return result

            #Empieza el bucle del for
            newLabel = generator.createLabel()
            tree.updateConsola(generator.newLabel(newLabel))
            LabelContador = generator.createLabel()

            #Utilizo el id de que guarda los caracteres 
            identificador = Identificador(self.identificador, self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            tempIdentificador = self.correctValue(identificador)

            #Compara si el caracter es igual a -1
            trueLabel = generator.createLabel()
            tree.updateConsola(generator.newIf(tempIdentificador, '-1', '!=', trueLabel))
            falseLabel = generator.createLabel()
            tree.updateConsola(generator.newGoto(falseLabel))

            tree.updateConsola(generator.newLabel(trueLabel))
            nuevaTabla = TablaSimbolos('for', nuevaTablaIntermedia)
            cantidad = len(expIzq.valor)
            for repeticiones in range(1, cantidad):
                for instruccion in self.instrucciones:

                    if isinstance(instruccion, Return): #Sentencia Return  
                        instruccion.label = falseLabel
                                
                    if isinstance(instruccion, Break): #Sentencia Break
                        instruccion.label = falseLabel

                    if isinstance(instruccion, Continue):
                        instruccion.label = LabelContador

                    if isinstance(instruccion, If):
                        instruccion.CONTINUE = LabelContador
                        instruccion.RETURN = falseLabel
                        instruccion.BREAK = falseLabel

                    resultIns = instruccion.interpretar(tree, nuevaTabla, generator)
                    if isinstance(resultIns, Excepcion):
                        tree.getExcepciones().append(resultIns)
                        tree.updateConsolaln(resultIns.toString())
                        
            tree.updateConsola(generator.newGoto(falseLabel))
            
            tree.updateConsola(generator.newPrint('c', '13'))    
            tree.updateConsola(generator.newGoto(str(LabelContador)))
            tree.updateConsola(generator.newLabel(LabelContador))

            uno = Number(1, Tipo.NUMBER, self.fila, self.columna)
            expIzq.tipo = Tipo.NUMBER
            IndiceCadena = Temporal(expIzq, self.fila, self.columna)
            suma = Suma(IndiceCadena, uno, self.fila, self.columna)

            asignacion = AsignacionVar('contador', suma, Tipo.NUMBER, self.fila, self.columna).interpretar(tree, nuevaTabla, generator)
            if isinstance(asignacion, Excepcion):
                return asignacion

            IndiceCadena = Identificador('contador', self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            ValorCadena = generator.createTemp()
            tree.updateConsola(generator.newGetHeap(ValorCadena, IndiceCadena.getTemporal()))
            valor = Value('', ValorCadena, Tipo.CADENA, True)
            ValorCadena = Temporal(valor, self.fila, self.columna)

            asignacion = AsignacionVar(self.identificador, ValorCadena, Tipo.CADENA, self.fila, self.columna).interpretar(tree, nuevaTabla, generator)
            if isinstance(asignacion, Excepcion):
                return asignacion

            tree.updateConsola(generator.newGoto(newLabel))
            tree.updateConsola(generator.newLabel(falseLabel))
            
        else:
            result = DeclaracionVar(self.identificador, self.expresionIzq, expresionIzqTipo, True, False, self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
            if isinstance(result, Excepcion):
                return result

            if self.expresionDer != None:
                expDer = self.expresionDer.interpretar(tree, nuevaTablaIntermedia, generator)
                if isinstance(expDer, Excepcion):
                    return expDer 
                

            newLabel = generator.createLabel()
            tree.updateConsola(generator.newLabel(newLabel))
            LabelContador = generator.createLabel() 
            
            if self.expresionDer.tipo == Tipo.BANDERA:
                
                identificador = Identificador(self.identificador, self.fila, self.columna)
                resultCondicion = MenorIgual(identificador, self.expresionDer.opDer, self.fila, self.columna).interpretar(tree, nuevaTablaIntermedia, generator)
                if isinstance(resultCondicion, Excepcion):
                    return resultCondicion

                tree.updateConsola(generator.newLabel(resultCondicion.trueLabel))
                nuevaTabla = TablaSimbolos('for', nuevaTablaIntermedia)
                for instruccion in self.instrucciones:

                    if isinstance(instruccion, Return): #Sentencia Return  
                        instruccion.label = resultCondicion.falseLabel
                                
                    if isinstance(instruccion, Break): #Sentencia Break
                        instruccion.label = resultCondicion.falseLabel

                    if isinstance(instruccion, Continue):
                        instruccion.label = LabelContador

                    if isinstance(instruccion, If):
                        instruccion.CONTINUE = LabelContador
                        instruccion.RETURN = resultCondicion.falseLabel
                        instruccion.BREAK = resultCondicion.falseLabel

                    resultIns = instruccion.interpretar(tree, nuevaTabla, generator)
                    if isinstance(resultIns, Excepcion):
                        tree.getExcepciones().append(resultIns)
                        tree.updateConsolaln(resultIns.toString())

                tree.updateConsola(generator.newPrint('c', '13'))    
                tree.updateConsola(generator.newGoto(str(LabelContador)))
                tree.updateConsola(generator.newLabel(LabelContador))       
                uno = Number(1, Tipo.NUMBER, self.fila, self.columna)
                suma = Suma(identificador, uno, self.fila, self.columna)

                asignacion = AsignacionVar(self.identificador, suma, Tipo.NUMBER, self.fila, self.columna).interpretar(tree, nuevaTabla, generator)
                if isinstance(asignacion, Excepcion):
                    return asignacion

                tree.updateConsola(generator.newGoto(newLabel))
                tree.updateConsola(generator.newLabel(resultCondicion.falseLabel))

            

    def getNode(self):
        return super().getNode()


    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()