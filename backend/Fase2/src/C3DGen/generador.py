from ..C3DGen.Nativas import *

class Generador:
    def __init__(self, indices):
        self.generador = None
        self.indices = indices
        self.temporal = 0
        self.label = 0 
        self.codigo = []
        self.listaTemporales = []
        self.modulo = False 
        self.LabelReturn = ''
        self.funcion = False

    def createTemp(self): #Generar un nuevo temporal
        self.temporal = self.indices['temporal']
        temporal = 't' + str(self.temporal)
        self.temporal += 1
        self.indices['temporal'] = self.temporal
        self.listaTemporales.append(temporal) #Se guarda para declararse
        return temporal

    def newAsigTemp(self, temp, valor):
        return temp + ' = ' + str(valor) + ';\n'

    def addAsigTemp(self, temp, valor):
        self.codigo.append(temp + ' = ' + str(valor) + ';')

#---------------------------------------------------------LABELS---------------------------------------------------------
    def createLabel(self):
        self.label = self.indices['label']
        label  = 'L' + str(self.label)
        self.label += 1
        self.indices['label'] = self.label
        return label

    def addLabel(self, label):
        self.codigo.append(str(label) + ":")

    def newLabel(self, label):
        if isinstance(label, list):
            labels = ''
            for l in label:
                labels += str(l)+":\n"
            return labels
        else:
            return str(label) + ":\n"

#---------------------------------------------------------FUNCIONES---------------------------------------------------------
    def addCallFunc(self, nombre):
        self.codigo.append(nombre+"();\n")

    def newCallFunc(self, nombre):
        return nombre+"();\n"

    def addReturn(self):
        self.codigo.append("return;\n")

    def newReturn(self):
        return "return;\n"

#---------------------------------------------------------ANY---------------------------------------------------------
    def addInstruction(self, instruction):
        self.codigo.append(instruction)

#---------------------------------------------------------IF---------------------------------------------------------
    def addIf(self, opIzq, opDer, operador, label):
        self.codigo.append("if(" + opIzq + " " + operador + " " + opDer + ") {goto " + label + ";}")

    def newIf(self, opIzq, opDer, operador, label):
        return "if(" + opIzq + " " + operador + " " + opDer + ") {goto " + label + ";}\n"

    def addGoto(self, label):
        self.codigo.append("goto " + label + ";")

    def newGoto(self, label):
        return "goto " + label + ";\n"

#---------------------------------------------------------EXPRESIONES---------------------------------------------------------
    def addExpresion(self, target, izq, der, operador): #Agrega las expresiones al codigo
        self.codigo.append(target + ' = ' + izq + ' ' + operador + ' ' + der + ';')

    def newExpresion(self, target, izq, der, operador): #Agrega las expresiones al codigo
        return target + ' = ' + izq + ' ' + operador + ' ' + der + ';\n'

    def addOpRelacional(self, expresion, trueIns, falseIns):
        newLabel = self.createLabel()
        if isinstance(expresion.trueLabel, list):
            for L in expresion.trueLabel:
                self.addLabel(str(L))
        else:
            self.addLabel(str(expresion.trueLabel))

        self.addInstruction(trueIns)
        self.addGoto(str(newLabel))
        if isinstance(expresion.falseLabel, list):
            for L in expresion.falseLabel:
                self.addLabel(str(L))
        else:
            self.addLabel(str(expresion.falseLabel))

        self.addInstruction(falseIns)
        self.addLabel(str(newLabel))

    def newOpRelacional(self, expresion, trueIns, falseIns):
        opRelacional = ''
        newLabel = self.createLabel()
        if isinstance(expresion.trueLabel, list):
            for L in expresion.trueLabel:
                opRelacional += self.newLabel(str(L))
        else:
            opRelacional += self.newLabel(str(expresion.trueLabel))

        opRelacional += trueIns
        opRelacional += self.newGoto(str(newLabel))
        if isinstance(expresion.falseLabel, list):
            for L in expresion.falseLabel:
                opRelacional +=  self.newLabel(str(L))
        else:
            opRelacional +=  self.newLabel(str(expresion.falseLabel))

        opRelacional += falseIns
        opRelacional +=  self.newLabel(str(newLabel))
        return opRelacional
        
#---------------------------------------------------------PRINT---------------------------------------------------------
    def addPrint(self, typePrint, value): #Añade un printf
        self.codigo.append('fmt.Printf(\"%' + typePrint + '\",' + value + ');')

    def newPrint(self, typePrint, value): #Añade un printf
        return 'fmt.Printf(\"%' + typePrint + '\",' + value + ');\n'

#---------------------------------------------------------NEWLINE---------------------------------------------------------
    def addNewLine(self):
        self.codigo.append('fmt.Printf(\"%c\",10);')

    def newNewLine(self):
        return 'fmt.Printf(\"%c\",10);\n'

#---------------------------------------------------------MANEJO DE MEMORIA HEAP---------------------------------------------------------
    def addGetHeap(self, target, index):
        self.codigo.append(target + " = heap[int(" + index + ")];")

    def newGetHeap(self, target, index):
        return target + " = heap[int(" + index + ")];\n"

    def addSetHeap(self, index, value):
        self.codigo.append("heap[int(" + index + ")] = " + value + ";" )

    def newSetHeap(self, index, value):
        return "heap[int(" + index + ")] = " + value + ";\n" 

    def addNextHeap(self):
        self.codigo.append("H = H + 1;")

    def newNextHeap(self):
        return "H = H + 1;\n"

#---------------------------------------------------------MANEJO DE MEMORIA STACK---------------------------------------------------------
    def addGetStack(self, target, index): #Obtiene el valor del stack en cierta posicion
        self.codigo.append(target+' = stack[int(' + index + ')];')

    def newGetStack(self, target, index): #Obtiene el valor del stack en cierta posicion
        return target+' = stack[int(' + index + ')];\n'

    def addSetStack(self, index, value): #Inserta valor del stack
        self.codigo.append('stack[int(' + index + ')] = ' + value + ';')

    def newSetStack(self, index, value): #Inserta valor del stack
        return 'stack[int(' + index + ')] = ' + value + ';\n'

    def addNextStack(self,index:str): #Se mueve hacia la posicion siguiente del stack
        self.codigo.append("P = P + " + index + ";")

    def newNextStack(self,index:str): #Se mueve hacia la posicion siguiente del stack
        return "P = P + " + index + ";\n"
    
    def addBackStack(self, index:str): #Se mueve hacia la posicion anterior del stack
        self.codigo.append("P = P - " + index + ";")

    def newBackStack(self, index:str): #Se mueve hacia la posicion anterior del stack
        return "P = P - " + index + ";\n"

    def newSimulateNextStack(self,target, index:str): #Se mueve hacia la posicion siguiente del stack de forma simulada
        return target +" = P + " + index + ";\n"

    def addSimulateNextStack(self,target, index:str): #Se mueve hacia la posicion siguiente del stack de forma simulada
        self.codigo.append(target +" = P + " + index + ";\n")

#---------------------------------------------------------MODULO---------------------------------------------------------
    def newModulo(self, dividendo, divisor):
        return "math.Mod(" + str(dividendo) + ", " + str(divisor) + ")"  

#---------------------------------------------------------GENERAR CODIGO---------------------------------------------------------
    def getCode(self, functionsCode):
        tempCode = 'package main\n'

        if self.modulo == True or functionsCode.modulo == True:
            tempCode += 'import ("math")\n'    

        tempCode += 'import ("fmt")\n'
        tempCode += 'var stack[30101999]float64;\n'
        tempCode += 'var heap[30101999]float64;\n'
        tempCode += 'var P, H float64;\n'
        tempCode += 'var '

        if len(functionsCode.listaTemporales) > 0:
            tempCode += functionsCode.getUsedTemps()
        tempCode += ','
        if len(self.listaTemporales) > 0:
            tempCode += self.getUsedTemps()
        tempCode += ' float64; \n\n'
        tempCode += addTrue()
        tempCode += addFalse()
        tempCode += addMathError()
        tempCode += addBoundsError()
        tempCode += "\n".join(functionsCode.codigo)
        tempCode += '\n\nfunc main(){\n'
        tempCode += "\n".join(self.codigo)
        tempCode += '}\n'

        return tempCode 


    def getUsedTemps(self):
        return ",".join(self.listaTemporales)

    