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

#----Base de datos-----

class Job(db.Model):
    __tablename__ = 'trabajos'

    id = db.Column(db.String(36), primary_key=True)
    input_ruta = db.Column(db.String(200), nullable=False)
    input_filtro = db.Column(db.String(50), default="grises")


def exportar_trabajo(job):

    status_bytes = redis_client.get(f"{job.id}:status")
    if status_bytes:
        status_real = status_bytes.decode('utf-8')
    else:
        status_real = "finished"

    data = {
        "job_id": job.id,
        "status": status_real,
        "input_ruta": job.input_ruta,
        "input_filtro": job.input_filtro,
        "uri": url_for('get_job_status', job_id=job.id, _external=True)
    }

    return data

with app.app_context():
    db.create_all()

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

    #para la base de datos
    nuevo_job = Job(id=job_id, input_ruta=ruta, input_filtro=filtro)
    db.session.add(nuevo_job)
    db.session.commit()

    #guardamos en redis 
    # estructura set job:clave-valor

    redis_client.set(f"{job_id}:status", "queued")

    redis_client.set(f"{job_id}:progress", 0)

    redis_client.set(f"{job_id}:input_filtro", filtro)

    redis_client.set(f"{job_id}:input_ruta", ruta)

    redis_client.set(f"{job_id}:result", "")

    redis_client.rpush('trabajos', job_id)


    return jsonify(exportar_trabajo(nuevo_job)), 201



@app.route('/jobs/<job_id>', methods=['GET'])
@auth.login_required
def get_job_status(job_id):

    existe_cliente = redis_client.exists(f"{job_id}:status")

    if not existe_cliente:
        abort(404)

    status = redis_client.get(f"{job_id}:status").decode('utf-8')
    progress = redis_client.get(f"{job_id}:progress").decode('utf-8')
    ruta = redis_client.get(f"{job_id}:input_ruta").decode('utf-8')
    filtro = redis_client.get(f"{job_id}:input_filtro").decode('utf-8')

    response = {
        "job_id": job_id,
        "status": status,
        "progress": progress,
        "input_ruta": ruta,
        "input_filtro": filtro,
        "uri": url_for('get_job_status', job_id=job_id, _external=True)
    }

    if status == "finished":
        result = redis_client.get(f"{job_id}:result")
        if result:
            cadena = result.decode('utf-8')
            partes = cadena.split(";")

            response["result"] = {
                "archivo": partes[0],
                "mensaje": partes[1] if len(partes) > 1 else ""
            }

    # Si falló
    elif status == "failed":
        response["error"] = "Error procesando la imagen"


    return jsonify(response), 200

@app.route('/jobs', methods=['GET'])
@auth.login_required
def get_jobs():

    trabajos = Job.query.all()
    exportados = [exportar_trabajo(t) for t in trabajos]

    return jsonify({"trabajos": exportados})

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
