# 🚀 Módulo P5: Distributed Asynchronous Image Processing Pipeline

Este módulo implementa un **sistema distribuido desacoplado** de alta concurrencia para procesamiento intensivo de imágenes utilizando una cola de tareas en memoria (**Redis**), un clúster de workers multiproceso (**NumPy + ProcessPoolExecutor**), una API RESTful (**Flask + Gunicorn**), persistencia relacional (**MariaDB + SQLAlchemy**) y un proxy inverso (**NGINX**).

---

## 🏗️ Arquitectura del Sistema

```
[ Cliente HTTP / Web / CLI ]
            │
            ▼ (Puerto 8080)
   ┌─────────────────┐
   │   NGINX Proxy   │
   └────────┬────────┘
            │ proxy_pass http://api:5000
            ▼
   ┌─────────────────┐       (Metadatos SQL)       ┌─────────────────┐
   │    API Flask    │ ──────────────────────────► │  MariaDB P5_db  │
   └────────┬────────┘                             └─────────────────┘
            │
            │ (1. RPUSH job_id a la cola 'trabajos')
            │ (2. SET job_id:status "queued")
            ▼
   ┌─────────────────┐
   │   Redis Queue   │
   └────────┬────────┘
            │
            │ (3. BLPOP bloqueante esperando trabajos)
            ▼
   ┌─────────────────┐
   │ Worker Procesor │ ──► Multi-threading (atención concurrente de jobs)
   │ (servidor_proc) │ ──► Multi-processing (ProcessPoolExecutor por chunks con NumPy)
   └────────┬────────┘
            │
            │ (4. Actualiza progreso en Redis: 0% ... 50% ... 100%)
            │ (5. Guarda imagen procesada en volumen compartido /static)
            ▼
   ┌─────────────────┐
   │ Volumen /static │
   └─────────────────┘
```

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.12
* **Broker & Cache:** Redis 7 (`redis-py`)
* **Base de Datos:** MariaDB (`Flask-SQLAlchemy`, `PyMySQL`)
* **Servidor Web & Proxy:** NGINX 1.29 + Gunicorn (4 workers)
* **Cómputo Paralelo:** `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, NumPy, Pillow
* **Seguridad:** HTTP Basic Auth con hashing criptográfico (`werkzeug.security`)
* **Orquestación:** Docker Compose (Red interna `bridge` con resolución DNS)

---

## 📡 Especificación de la API REST

Todos los endpoints requieren autenticación HTTP Basic (`alumno:alumno_pass`).

### 1. Crear un trabajo de procesamiento
* **Endpoint:** `POST /jobs`
* **Cabeceras:** `Content-Type: application/json`
* **Cuerpo de la petición:**
```json
{
  "ruta": "static/ejemplo.png",
  "filtro": "sepia"
}
```
*(Filtros disponibles: `grises`, `sepia`, `blur`)*

* **Respuesta (`201 Created`):**
```json
{
  "job_id": "5a6a48b1-d158-4e1f-8e29-64af60958d02",
  "status": "queued",
  "input_ruta": "static/ejemplo.png",
  "input_filtro": "sepia",
  "uri": "http://localhost:8080/jobs/5a6a48b1-d158-4e1f-8e29-64af60958d02"
}
```

---

### 2. Consultar el estado y progreso de un trabajo
* **Endpoint:** `GET /jobs/<job_id>`
* **Respuesta en progreso (`200 OK`):**
```json
{
  "job_id": "5a6a48b1-d158-4e1f-8e29-64af60958d02",
  "status": "processing",
  "progress": "66",
  "input_ruta": "static/ejemplo.png",
  "input_filtro": "sepia",
  "uri": "http://localhost:8080/jobs/5a6a48b1-d158-4e1f-8e29-64af60958d02"
}
```

* **Respuesta al finalizar (`200 OK`):**
```json
{
  "job_id": "5a6a48b1-d158-4e1f-8e29-64af60958d02",
  "status": "finished",
  "progress": "100",
  "result": {
    "archivo": "ejemplo_sepia.png",
    "mensaje": "Procesado correctamente"
  },
  "uri": "http://localhost:8080/jobs/5a6a48b1-d158-4e1f-8e29-64af60958d02"
}
```

---

### 3. Listar todos los trabajos registrados
* **Endpoint:** `GET /jobs`
* **Respuesta (`200 OK`):**
```json
{
  "trabajos": [
    {
      "job_id": "5a6a48b1-d158-4e1f-8e29-64af60958d02",
      "status": "finished",
      "input_ruta": "static/ejemplo.png",
      "input_filtro": "sepia"
    }
  ]
}
```

---

## 💻 Cliente CLI de Línea de Comandos
El sistema incluye una herramienta CLI desarrollada con la librería `Click` para interactuar con la API sin necesidad de navegador:

```bash
# Enviar un nuevo trabajo
python backend/cliente.py new static/docker.png --filtro grises

# Consultar el estado de un trabajo por ID
python backend/cliente.py status 5a6a48b1-d158-4e1f-8e29-64af60958d02

# Listar todos los trabajos ejecutados
python backend/cliente.py list
```

---

## 🚀 Despliegue con Docker Compose

```bash
# 1. Navegar al directorio de despliegue
cd compose-ej1

# 2. Levantar la infraestructura completa en segundo plano
docker compose up -d --build

# 3. Comprobar los 5 contenedores en ejecución
docker compose ps
```

* **Interfaz Web:** Abre `http://localhost:8080/static/main-auth.html`
* **API REST:** Escuchando en `http://localhost:8080/jobs`
