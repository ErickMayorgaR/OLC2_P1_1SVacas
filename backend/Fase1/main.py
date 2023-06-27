from flask import Flask, jsonify, request
from flask_cors import CORS
from jinja2 import Template
from Analizador_Sintactico import parse, errores, agregarNativas
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
from src.TS.Excepcion import Excepcion
from src.Instrucciones.Funcion.Funcion import Funcion
from src.Instrucciones.Structs.Struct import Struct
import subprocess
import graphviz

#======================================================================================================#
def TablaErrores(errores):
    template = Template(open('tabla_errores.html').read())
    return template.render(errores=errores)

def TablaSimbolosHTML(simbolos):
    template = Template(open('tabla_simbolos.html', encoding='utf-8').read())
    return template.render(simbolos=simbolos)

#======================================================================================================#
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
#======================================================================================================#


app = Flask(__name__)
CORS(app)

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
    agregarNativas(ast)

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
    salida = ast.getConsola()
    # simbolos = TablaSimbolosHTML(TSGlobal.getSimbolos())
    grafo = generarAST(ast)
    with open('ast.dot', 'w') as file:
        file.write(grafo)

    # Ruta al archivo .dot
    ruta_dot = "ast.dot"

    # Ruta de salida para la imagen generada
    ruta_imagen = "ast.png"

    # Ejecutar el comando "dot" para generar la imagen
    comando_dot = f"dot -Tpng -Gcharset=latin1 {ruta_dot} -o {ruta_imagen}"
    subprocess.run(comando_dot, shell=True)

    return jsonify({'salida': salida, 'grafo' : grafo, 'errores':erroress})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


   