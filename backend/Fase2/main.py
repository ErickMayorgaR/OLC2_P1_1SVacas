from flask import Flask, jsonify, request
from flask_cors import CORS
from Analizador_Sintactico import parse, errores
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
from src.TS.Excepcion import Excepcion



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

    for error in errores: #Captura de errores lexicos y sintacticos 
        ast.getExcepciones().append(error)
        ast.updateConsolaln(error.toString())

    for instruccion in ast.getInstrucciones():
        valor = instruccion.interpretar(ast, TSGlobal)
        if isinstance(valor, Excepcion):
            ast.getExcepciones().append(valor)
            ast.updateConsolaln(valor.toString())
    salida = ast.getConsola()

    return jsonify({'salida': salida})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


   