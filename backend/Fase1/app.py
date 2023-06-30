from flask import Flask, jsonify, request
from flask_cors import CORS
from Analizador_Sintactico import parse, errores
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
from src.TS.Excepcion import Excepcion
import subprocess
import graphviz



app = Flask(__name__)
CORS(app)

def generarAST(ast):
    from src.Abstract.NodeCst import NodeCst
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


@app.route("/")
def hello():
    return "Hello, World!"

'''Se define la ruta para la entrada, utiliza la entrada para ejecutar el analizador, 
devuelve la salida interpretada '''
@app.route('/entrada', methods = ['POST']) 
def recibirDatos():
    salida = ""
    entrada = request.json['entrada']

    instrucciones = parse(entrada) #ARBOL AST
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos('global')
    ast.setTSGlobal(TSGlobal)

    for error in errores: #Captura de errores lexicos y sintacticos 
        ast.getExcepciones().append(error)

    for instruccion in ast.getInstrucciones():
        valor = instruccion.interpretar(ast, TSGlobal)
        if isinstance(valor, Excepcion):
            ast.getExcepciones().append(valor)
    salida = ast.getConsola()

    simbolos = TSGlobal.getSimbolosJSON()

    grafo = generarAST(ast)
    with open('ast.dot', 'w') as file:
        file.write(grafo)

    # Ruta al archivo .dot
    ruta_dot = "ast.dot"
    pdf_file = "ast"

    graph = graphviz.Source.from_file(ruta_dot)
    graph.format = 'pdf'
    graph.render(filename=pdf_file, cleanup=True)


    # # Ruta de salida para la imagen generada
    # ruta_imagen = "ast.png"

    # # Ejecutar el comando "dot" para generar la imagen
    # comando_dot = f"dot -Tpng -Gcharset=latin1 {ruta_dot} -o {ruta_imagen}"
    # subprocess.run(comando_dot, shell=True)


    return jsonify({'salida': salida, 'tablaSimbolos': simbolos, 'errores': ast.getExcepcionesJSON()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


   