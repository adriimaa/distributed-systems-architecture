# coding: utf-8
from flask import Flask, jsonify,abort, make_response, request

app = Flask(__name__)

tareas = [  # Es una lista
    { # Cada tarea es un diccionario
      'id': 1,
      'descripcion': 'Terminar práctica Hola Mundo con Flask',
      'completada': True
    },
    {
      'id': 2,
      'descripcion': 'Terminar práctica aplicación To-Do',
      'completada': False
    }
]

def buscar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            return tarea
        return None

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
    return jsonify({"tareas": tareas})

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify({ 'tarea': tarea})

@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def solicitud_incorrecta(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)

@app.route("/lista/v1/tareas", methods=["POST"])
def create_tarea():
    if not request.json:
        abort(400)
    
    if 'descripcion' not in request.json:
        abort(400)
    
    if 'completada' in request.json:
        if type(request.json['completada'])== bool:
            estado = request.json['completada']

    nueva_tarea = {
        'id': tareas[-1]['id'] + 1,
        'descripcion': request.json['descripcion'],
        'completada': estado
    }

    tareas.append(nueva_tarea)

    return jsonify({'tarea': nueva_tarea}), 201

@app.route('/lista/v1/tarea/<int:id>', methods=["PUT"])
def update_tarea(id):
        tarea = buscar_tarea(id)
        if tarea is None:
                abort(404)
        if not request.json:
                abort(400)
        if 'descripcion' in request.json:
                if type(request.json['descripcion'])!=str:
                        abort(400)
                tarea['descripcion'] = request.json['descripcion']
        if 'completada' in request.json:
                if type(request.json['completada'])!=bool:
                        abort(400)
                tarea['completada'] = request.json['completada']
        return make_response(jsonify({'tarea': tarea}), 200)
