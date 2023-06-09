from flask import Flask, jsonify, request
from flask_cors import CORS

from Analizador_Sintactico import parse


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
    instrucciones = parse(entrada)
    
    for instruccion in instrucciones:
        salida += instruccion.interpretar(None,None) + "\n"
    #Se llama al analizador lexico
    return jsonify({'salida': salida})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


   