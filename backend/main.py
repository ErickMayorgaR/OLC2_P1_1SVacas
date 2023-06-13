from src.Instrucciones.Funcion.Funcion import Funcion
from ..backend.Analizador_Sintactico import parse, crearNativas, errores
from src.Instrucciones.Structs.Struct import Struct
from src.TS.TablaSimbolos import TablaSimbolos
from flask import Flask, jsonify, request
from src.TS.Excepcion import Excepcion
from src.TS.Arbol import Arbol
from flask_cors import CORS

#======================================================================================================#
def TablaErrores(errores):
    import webbrowser
    file = open('TablaErrores.html', 'w')
    cadena =""
    i = 0
    for error in errores:
        if error.tipo.lower() == 'semántico' or error.tipo.lower() == 'sematico':
            i += 1
            cadena +="<tr>\n"\
            "<td> "+str(i)+" </td>\n"\
            "<td> "+str(error.tipo)+" </td>\n"\
            "<td> "+str(error.descripcion)+" </td>\n"\
            "<td> "+str(error.fila)+" </td>\n"\
            "<td> "+str(error.columna)+" </td>\n"\
            "<td> "+str(error.fecha)+" </td>\n"\
            "<td> "+str(error.hora)+" </td>\n"\
            "</tr>\n"\

    return codigoHTML(cadena)
    '''file.write(codigoHTML(cadena))
    file.close()
    webbrowser.open_new_tab('TablaErrores.html')
'''


def codigoHTML(tabla):
    cadena = "<html>\n"\
            "<head></head>\n"\
            "<body>\n"\
            "<div>\n"\
            "<center>\n"\
            "<h2>Tabla de errores</h2>\n"\
            "</center>\n"\
            "</div>\n"\
            "<br> <br> <br> <br> <br> <br>\n"\
            "<center>\n"\
            "<table border=\"1\">\n"\
            "<tr>\n"\
            "<th>Numero</th>\n"\
            "<th>Tipo</th>\n"\
            "<th>Descripcion</th>\n"\
            "<th>Fila</th>\n"\
            "<th>Columna</th>\n"\
            "<th>Fecha</th>\n"\
            "<th>Hora</th>\n"\
            "</tr>\n"
    cadena += tabla
    cadena += "</center>\n"\
            "</table>\n"\
            "</body>\n"\
            "</html>\n"
    return cadena

#======================================================================================================#
def generarAST(ast):
    from .src.Abstract.NodeCst import NodeCst
    import os
    
    inicio = NodeCst("RAIZ")
    instrucciones = NodeCst("instrucciones")
    instruccion = NodeCst("instruccion")

    for instruccionn in ast.getInstrucciones():
        instruccion.addChildNode(instruccionn.getNode())

    instrucciones.addChildNode(instruccion)
    inicio.addChildNode(instrucciones)
    grafo = ast.getDot(inicio)

    return grafo
#======================================================================================================#


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/compiler', methods=["POST"])
def noseque():
    entrada = request.json["codigo"]
    instrucciones = parse(entrada) #ARBOL AST
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos('global')
    ast.setTSGlobal(TSGlobal)
    crearNativas(ast)

    for error in errores: #Captura de errores lexicos y sintacticos 
        ast.getExcepciones().append(error)
        ast.updateConsolaln(error.toString())
    

    for instruccion in ast.getInstrucciones():
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)
        elif isinstance(instruccion, Struct):
            ast.addStruct(instruccion)
        else:
            valor = instruccion.interpretar(ast, TSGlobal)
            if isinstance(valor, Excepcion):
                ast.getExcepciones().append(valor)
                ast.updateConsolaln(valor.toString())
        
    erroress = TablaErrores(ast.getExcepciones())
    grafo = generarAST(ast)
        
    return jsonify({'salida': ast.getConsola(), 'grafo' : grafo, 'errores':erroress})

if __name__ == '__main__':
    app.run(debug=True, port=4000)

