from ..TS.Excepcion import Excepcion
class TablaSimbolos:
    def __init__(self, owner, anterior = None):
        self.tabla = {} #Da un diccionario vacio
        self.owner = owner
        self.anterior = anterior

    def setTabla(self, simbolo): #Agrega una variable al entorno
        if simbolo.identificador in self.tabla:
            return True
            #return Excepcion("Semántico", "Variable \"" + simbolo.identificador + "\" ya existe", simbolo.fila, simbolo.columna)
        else:  
            self.tabla[simbolo.getID()] = simbolo
            return None

    def getTabla(self, identificador):
        tablaActual = self
        while tablaActual != None:
            if identificador in tablaActual.tabla:
                return tablaActual.tabla[identificador] #Devuelve un nodo simbolo
            else:
                tablaActual = tablaActual.anterior
        return None

    def getSimbolos(self):
        tablaActual = self
        simbolos = []
        for symbol in tablaActual.tabla:
            simbolos.append(symbol)
        return simbolos
    
    def getSimbolosJSON(self):
        tablaActual = self
        simbolos = []
        for symbol in tablaActual.tabla.values():
            simbolos.append(symbol.getJsonSymbol())
        return simbolos

    def getRealTabla(self, identificador):
        tablaActual = self
        while tablaActual != None:
            if identificador in tablaActual.tabla:
                return tablaActual #Devuelve un nodo simbolo
            else:
                tablaActual = tablaActual.anterior
        return None

    def getNombreTabla(self):
        tablaActual = self
        while tablaActual != None:
            if tablaActual.owner == 'function':
                return True #Avisa si hay un entorno de function en el medio
            else:
                tablaActual = tablaActual.anterior
        return False

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.identificador in tablaActual.tabla:
                tablaActual.tabla[simbolo.identificador].setValor(simbolo.getValor())
                tablaActual.tabla[simbolo.identificador].setTipo(simbolo.getTipo())
                return "variable actualizada" #Si regresa esto es que si la actualizo
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable no encontrada.", simbolo.getFila(), simbolo.getColumna()) 