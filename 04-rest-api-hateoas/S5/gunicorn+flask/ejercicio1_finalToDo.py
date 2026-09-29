# coding: utf-8
import os
from flask import Flask, jsonify,abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash


auth = HTTPBasicAuth()
auth.realm = "Es necesario autenticarse"

autorizados = {}  # Ninguno de momento, los cargaremos de fichero

def leer_usuarios_autorizados(nombre_fichero):
    try:
        lineas = open(nombre_fichero, "r").readlines()
    except:
        # Si no se ha podido abrir el fichero, no seguimos
        return
    # En caso contrario leemos el fichero para rellenar el diccionario
    # de usuarios autorizados
    for linea in lineas:
        linea = linea.strip()  # Eliminar retorno de carro
        if not linea:
            continue    # Saltar lineas vacías
        usuario, contraseña = linea.split()
        autorizados[usuario] = contraseña

leer_usuarios_autorizados("contrasenyas.txt")

@auth.verify_password
def verificar(usuario, contraseña):
    # Esta función debe retornar True si la el usuario/contraseña es válido
    # y False en caso contrario
    if usuario in autorizados:
        return check_password_hash(autorizados[usuario], contraseña)
    else:
        return False

@auth.error_handler
def no_autorizado():
    # Esta función debe retornar la respuesta en caso de error de
    # autenticación, que se produce si el cliente no envía la cabecera
    # Authenticate, o si el usuario enviado no se encuentra, o si
    # la clave proporcionada no encaja con la esperada.
    # Elegimos retornar un código 401 (Unauthorized) para este caso
	return make_response(jsonify({'error': 'Credenciales no válidas'}), 401)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI',
     'mysql+pymysql://tarea_user:tarea_pass@mariadb_tarea_db/tarea_db')
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
		'completada': tarea.completada,
        'uri': url_for('get_tarea', id=tarea.id, _external=True)
	}

@app.route("/lista/v1/tareas", methods=["GET"])
@auth.login_required
def get_tareas():
	tareas = Tarea.query.all()  # 7
	exportadas = [exportar_tarea(t) for t in tareas]
	return jsonify({"tareas": exportadas})

@app.route("/lista/v1/tarea/<int:id>", methods=["GET"])
@auth.login_required
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
@auth.login_required
def create_tarea():
    if not request.json:
        abort(400)

    if 'descripcion' not in request.json:
        abort(400)

    nueva_tarea = Tarea(descripcion=request.json['descripcion'],completada=request.json.get('completada', False))
    db.session.add(nueva_tarea)
    db.session.commit()

    return jsonify({'tarea': exportar_tarea(nueva_tarea)}), 201

@app.route('/lista/v1/tarea/<int:id>', methods=["PUT"])
@auth.login_required
def update_tarea(id):

    tarea = Tarea.query.get(id)
    if tarea is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'descripcion' in request.json:
        if type(request.json['descripcion'])!=str:
            abort(400)
        tarea.descripcion = request.json['descripcion']

    if 'completada' in request.json:
        if type(request.json['completada'])!=bool:
            abort(400)
        tarea.completada = request.json['completada']
        
    db.session.commit()

    return jsonify({'tarea': exportar_tarea(tarea)}), 200

@app.route('/lista/v1/tarea/<int:id>', methods=["DELETE"])
@auth.login_required
def delete_tarea(id):
    t = Tarea.query.get(id)

    if t is None:
        abort(404)

    db.session.delete(t)
    db.session.commit()

    return jsonify({'borrado': True}), 200

def url_tarea(tarea):
    tarea_actualizada = {
        'descripcion' : tarea.descripcion,
        'completada' : tarea.completada,
        'uri' : url_for('get_tarea', id = tarea.id, _external=True)}
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