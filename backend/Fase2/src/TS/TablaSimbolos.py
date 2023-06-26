class TablaSimbolos:
    def __init__(self, owner, anterior = None):
        self.tabla = {}
        self.owner = owner
        self.anterior = anterior
        self.size = 0
        self.ownSize = 0

        if anterior != None:
            self.size = anterior.size

    def setTabla(self, simbolo): #Agrega una variable al entorno
        if simbolo.identificador in self.tabla:
            return True
        else:
            self.tabla[simbolo.identificador] = simbolo
            self.size += 1
            self.ownSize += 1
            return None

    def changeOwnSize(self, tam):
        self.ownSize += tam

    def getTabla(self, identificador):
        tablaActual = self
        while tablaActual != None:
            if identificador in tablaActual.tabla:
                return tablaActual.tabla[identificador] #Devuelve un nodo simbolo
            else:
                tablaActual = tablaActual.anterior
        return None

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
        return None #Si regresa esto es que no la actualizo
    