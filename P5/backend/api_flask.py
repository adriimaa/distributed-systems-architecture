import os
from flask import Flask, jsonify,abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import redis
import uuid
import json
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
#Creamos una nueva base de datos para esta práctica P5_db para guardar los trabajos.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI',
'mysql+pymysql://tarea_user:tarea_pass@mariadb_P5_db/P5_db')
db = SQLAlchemy(app)

#Utilizamos la misma forma de autenticación y main-auth.html que en practica anterior----
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

#---Hay q hacer la tabla trabajos (base de datos)----



#----Redis----
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

@app.route('/jobs', methods=['POST'])
@auth.login_required
def create_job():
    data = request.json
    if not data or 'ruta' not in data:
         abort(400)

    ruta = request.json['ruta']
    filtro = request.json.get('filtro', 'grises')

    filtros_validos = ['grises', 'sepia', 'blur']

    if not os.path.exists(ruta) or filtro not in filtros_validos:
        abort(400)

    #generar id único
    job_id = str(uuid.uuid4())

    #guardamos en redis 
    # estructura set job:clave-valor

    redis_client.set(f"{job_id}:status", "queued")

    redis_client.set(f"{job_id}:progress", 0)

    redis_client.set(f"{job_id}:input_filtro", filtro)

    redis_client.set(f"{job_id}:input_ruta", ruta)

    redis_client.set(f"{job_id}:result", "")

    redis_client.rpush('trabajos', job_id)

    data = {
        "job_id": job_id,
        "status": "queued",
        "input_ruta": ruta,
        "input_filtro": filtro,
        "uri": url_for('get_job_status', job_id=job_id, _external=True)
    }

    return jsonify(data), 201


@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    return "prueba"



#manejo de errores
@app.errorhandler(404)
def no_encontrado(error):
    return make_response(jsonify({'error': 'Trabajo inexistente'}), 404)

@app.errorhandler(400)
def solicitud_incorrecta(error):
    return make_response(jsonify({'error': 'Solicitud incorrecta se requiere que la ruta y el filtro sean correctos'}), 400)

# Permitir CORS
#
# Añadimos esta cabecera a todas las respuestas que generemos
@app.after_request
def after(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers','content-type, authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PUT, DELETE')
    return response
