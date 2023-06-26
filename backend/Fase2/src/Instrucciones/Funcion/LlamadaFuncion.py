from ...Abstract.abstract import Instruccion
from ...TS.TablaSimbolos import TablaSimbolos
from ...TS.Excepcion import Excepcion
from ...TS.Simbolo import Simbolo
from ...TS.Valor import Value
from ...TS.Tipo import Tipo


class LlamadaFuncion(Instruccion):
    def __init__(self, identificador, parametros, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO

    def interpretar(self, tree, table, generator):
        funcion = tree.getFuncion(str(self.identificador))
        struct = 'tree.getStruct(str(self.identificador))'

        if funcion != None: #Para las funciones
            if generator.funcion == True:
                ultimoTemp = generator.temporal-1
                self.agregarRecursion(tree, table, generator, tree.getConsola(), funcion.Temporales, funcion.primerTemp, ultimoTemp)
            
            if len(funcion.parametros) != len(self.parametros):
                return Excepcion("Semántico", "Cantidad de parámetros incorrecta en función \""+self.identificador+"\"", self.fila, self.columna)

            tamTabla = table.size
            newTemp = generator.createTemp()                                #Temp cambio simulado de ambito
            tree.updateConsola(generator.newSimulateNextStack(newTemp, str(tamTabla))) #Cambio simulado de ambito           

            contador = 0
            for expresion in self.parametros:
                newTempIndice = generator.createTemp()                                #Temp cambio simulado de ambito
                tree.updateConsola(generator.newExpresion(newTempIndice, newTemp, str(contador+1), '+')) #Cambio simulado de ambito           


                resultExpresion = expresion.interpretar(tree, table, generator) #cambio
                if isinstance(resultExpresion, Excepcion):
                    return resultExpresion

                #Para poder capturar el tipo de dato de la variable y asi no modificar el verdadero sino el momentaneo jeje
                if funcion.parametros[contador]['identificador'].lower() == 'truncate$$parametros123' or funcion.parametros[contador]['identificador'].lower() == 'typeof$$parametros123' or funcion.parametros[contador]['identificador'].lower() == 'sin$$parametros123' or funcion.parametros[contador]['identificador'].lower() == 'cos$$parametros123' or funcion.parametros[contador]['identificador'].lower() == 'tan$$parametros123':
                    funcion.parametros[contador]['tipo'] = expresion.tipo

                if funcion.parametros[contador]['tipo'] != expresion.tipo and funcion.parametros[contador]['tipo'] != None: #Verifica que los parametros sean del mismo tipo
                    return Excepcion("Semántico", "Tipo de dato diferente en parámetros en la función \""+self.identificador+"\"", self.fila, self.columna)

                
                value = self.correctValue(resultExpresion)
                tree.updateConsola(generator.newSetStack(newTempIndice, str(value)))
                contador += 1


            tree.updateConsola(generator.newNextStack(str(tamTabla)))  #Cambia de ambito
            tree.updateConsola(generator.newCallFunc(self.identificador)) #Llama a la funcion

            newTempIndiceReturn = generator.createTemp()
            tree.updateConsola(generator.newExpresion(newTempIndiceReturn, 'P', '0', '+'))
            
            newTempValorReturn = generator.createTemp()    #Tiene el valor de return 
            tree.updateConsola(generator.newGetStack(newTempValorReturn, newTempIndiceReturn))

            tree.updateConsola(generator.newBackStack(str(tamTabla)))  #Regresa en el ambito
            
            if generator.funcion == True:
                self.devolverRecursion(tree, generator, funcion.Temporales)
            
            self.tipo = funcion.tipo
            valor = Value('', newTempValorReturn, self.tipo, True) #Retornando temporal
            return valor

        elif struct != None: #Para las structs
            pass

        elif struct == None and funcion == None: #Por si no existe nada jsjs
            return Excepcion("Semántico", "Struct/Funcion \""+self.identificador+"\" no encontrado", self.fila, self.columna)


    def getNode(self):
        return super().getNode()

    def agregarRecursion(self, tree, table, generator, funcion, temporales, primerTemp, ultimoTemp):
        print("-------------------------------------------------")
        print(primerTemp)
        print(ultimoTemp)
        print("-------------------------------------------------")
        print(funcion)
        print("-------------------------------------------------")
        for iterador in range(primerTemp,ultimoTemp+1):
            apariciones = funcion.count('t'+str(iterador))
            if apariciones == 1:
                print('t'+str(iterador), apariciones)
                temp = 't'+str(iterador)
                if temp in temporales:
                    tempOfTemp = generator.createTemp()
                    tree.updateConsola(generator.newExpresion(tempOfTemp, 'P', str(temporales[temp]), '+'))
                    tree.updateConsola(generator.newSetStack(tempOfTemp, temp))
                else:
                    temporales[temp] = table.size
                    table.size += 1
                    
                    tempOfTemp = generator.createTemp()
                    tree.updateConsola(generator.newExpresion(tempOfTemp, 'P', str(temporales[temp]), '+'))
                    tree.updateConsola(generator.newSetStack(tempOfTemp, temp))

                

        print("-------------------------------------------------")
        print(temporales)

    def devolverRecursion(self, tree, generator, temporales):
        print("-------------------------------------------------")
        for clave in temporales:
            tempOfTemp = generator.createTemp()
            tree.updateConsola(generator.newExpresion(tempOfTemp, 'P', str(temporales[clave]), '+'))
            tree.updateConsola(generator.newGetStack(str(clave), tempOfTemp))
        print("-------------------------------------------------")

    def correctValue(self, valor):
        if valor.isTemp:
            return valor.getTemporal()
        else:
            return valor.getValor()