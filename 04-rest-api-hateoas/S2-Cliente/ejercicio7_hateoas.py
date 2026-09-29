# coding: utf-8
from flask import Flask, jsonify,abort, make_response, request, url_for

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
    tareas_url = [url_tarea(t) for t in tareas]
    return jsonify({"tareas": tareas_url})

@app.route('/lista/v1/tarea/<int:id>', methods=["GET"])
def get_tarea(id):
    tarea = buscar_tarea(id)
    if tarea is None:
        abort(404)
    return jsonify({ 'tarea': url_tarea(tarea)})

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

    estado = False
    if 'completada' in request.json:
        if type(request.json['completada'])== bool:
            estado = request.json['completada']

    #Si la lista esta vacia id: 1
    if len(tareas) == 0:
        nuevo_id = 1
    else:
        nuevo_id = tareas[-1]['id'] + 1

    nueva_tarea = {
        'id': nuevo_id,
        'descripcion': request.json['descripcion'],
        'completada': estado
    }

    tareas.append(nueva_tarea)

    return jsonify({'tarea': url_tarea(nueva_tarea)}), 201

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
        return jsonify({'tarea': url_tarea(tarea)}), 200

@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
def delete_tarea(id):
    tarea = buscar_tarea(id)

    if tarea is None:
        abort(404)

    tareas.remove(tarea)

    return jsonify({'borrado': True}), 200

def url_tarea(tarea):
    tarea_actualizada = {
        'descripcion' : tarea['descripcion'],
        'completada' : tarea['completada'],
        'uri' : url_for('get_tarea', id = tarea['id'], _external=True)}
    return tarea_actualizada 

# Permitir CORS
#
# Añadimos esta cabecera a todas las respuestas que generemos
@app.after_request
def after(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers','content-type, authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PUT, DELETE')
    return response