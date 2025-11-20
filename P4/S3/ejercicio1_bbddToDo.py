# coding: utf-8
from flask import Flask, jsonify,abort, make_response, request, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tarea_user:tarea_pass@localhost/tarea_db'
db = SQLAlchemy(app)


class Tarea(db.Model):  # 1
	"""
    Definición de la tabla 'tareas' de la base de datos
    """

	__tablename__ = "tareas"  # 2

	id = db.Column(db.Integer, primary_key=True)  # 3
	descripcion = db.Column(db.String(100), nullable=False)
	completada = db.Column(db.Boolean(create_constraint=True), default=False)

	# Podemos escribir la función siguiente para implementar cómo debe
    # mostrarse un objeto de esta clase si lo imprimes desde python
	def __repr__(self):  # 4
		return "<Tarea[{}]: {} - {}>".format(self.id, self.descripcion, self.completada)

# def busca_tarea(id) ya no es necesaria  # 5

# Función auxiliar recomendada en la Práctica 4 - Parte 2 (Ejercicio 7)
def exportar_tarea(tarea):  # 6
	# print(tarea)
	return {
		"descripcion": tarea.descripcion,
		"completada": ..., # COMPLETAR
		'completada': tarea.completada,
        'uri': url_for('get_tarea', id=tarea.id, _external=True)
	}

@app.route("/lista/v1/tareas", methods=["GET"])
def get_tareas():
	tareas = Tarea.query.all()  # 7
	exportadas = [exportar_tarea(t) for t in tareas]
	return jsonify({"tareas": exportadas})

@app.route("/lista/v1/tarea/<int:id>", methods=["GET"])
def get_tarea(id):
	tarea = Tarea.query.get(id)  # 8
	if tarea:
		return jsonify({ "tarea": exportar_tarea(tarea) })
	else:
		abort(404)

# Crea las tablas en la base de datos (si aún no existen)
with app.app_context():  # 9
	db.create_all()

@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Tarea inexistente'}), 404)

@app.errorhandler(400)
def solicitud_incorrecta(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta'}), 400)

#Crear Nuevas funciones.
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