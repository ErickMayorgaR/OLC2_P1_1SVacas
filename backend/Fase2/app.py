from flask import Flask, jsonify, request
from flask_cors import CORS
from Analizador_Sintactico import parse, errores
from src.TS.Arbol import Arbol
from src.TS.TablaSimbolos import TablaSimbolos
from src.TS.Excepcion import Excepcion
from src.Instrucciones.Funcion.Funcion import Funcion
from Analizador_Sintactico import crearNativas
from src.C3DGen.generador import Generador



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
    label = 0
    temporal = 0
    indices = {'temporal' : 0, 'label' : 0}
    generator = Generador(indices)

    generatorFunction = Generador(indices)
    generatorFunction.funcion = True
    crearNativas(ast)

    for func in ast.getFunciones():
        valor = func.interpretar(ast, TSGlobal, generatorFunction)
        if isinstance(valor, Excepcion):
            ast.getExcepciones().append(valor)
            ast.setConsola('')
        else:
            generatorFunction.addInstruction(ast.getConsola())
            ast.setConsola('')


    for error in errores: #Captura de errores lexicos y sintacticos 
        ast.getExcepciones().append(error)
        ast.updateConsolaln(error.toString())


    for instruccion in ast.getInstrucciones():
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)
            valor = instruccion.interpretar(ast, TSGlobal, generatorFunction)
            generatorFunction.LabelReturn = ''
        else:
            valor = instruccion.interpretar(ast, TSGlobal, generator)
            
        if isinstance(valor, Excepcion):
            ast.getExcepciones().append(valor)
            ast.setConsola('')
        else:
            if isinstance(instruccion, Funcion):
                generatorFunction.addInstruction(ast.getConsola())
                ast.setConsola('')
            else:
                generator.addInstruction(ast.getConsola())
                ast.setConsola('')
    salida = generator.getCode(generatorFunction)

    return jsonify({'salida': salida})

if __name__ == '__main__':
    app.run(debug=True, port=3800)


   