# 🌐 Distributed Systems & Cloud Architecture Portfolio
> **Asignatura:** Sistemas Distribuidos | Grado en Ciencia e Ingeniería de Datos  
> **Autores:** [Adrián Manso Martínez](https://github.com/adriimaa) & Yonathan Patricio Torrejón Martínez  
> **Memoria Completa:** [📄 Ver Documentación Técnica Oficial (79 páginas PDF)](./docs/Memoria_Sistemas_Distribuidos.pdf)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Queue%20%26%20Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-SQL-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-Reverse%20Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Parallel%20Compute-013243?style=for-the-badge&logo=numpy&logoColor=white)

---

## 📌 Resumen del Repositorio

Este repositorio recoge la evolución completa en el diseño, desarrollo y despliegue de **sistemas distribuidos, protocolos de red, arquitecturas orientadas a eventos y microservicios contenerizados**.

El código abarca desde la implementación de protocolos fiables sobre capas de transporte (UDP/TCP) hasta la arquitectura de producción de un **sistema distribuido de procesamiento asíncrono de tareas pesadas orquestado con Docker Compose (Proyecto Estrella P5)**.

---

## 🚀 PROYECTO ESTRELLA: Pipeline Distribuido de Procesamiento Asíncrono ([Directorio P5](./P5))

Sistema desacoplado basado en el patrón **Productor-Consumidor (Task Queue)** para procesar transformaciones intensivas de imágenes en CPU de manera asíncrona y escalable.

### 📐 Diagrama de Arquitectura

```mermaid
flowchart TD
    subgraph Exterior
        Client[Cliente Web / CLI / HTTPie]
    end

    subgraph "Infraestructura Docker Compose (Red Privada)"
        Nginx[Proxy Inverso NGINX :8080]
        API[API REST Flask :5000<br/>Gunicorn 4 Workers]
        Redis[(Redis In-Memory Broker<br/>Cola 'trabajos' + Estado)]
        DB[(MariaDB SQL<br/>Persistencia Histórica)]
        Worker[Worker de Cómputo<br/>servidor_proc.py]
        Volume[(Volumen Compartido /static)]
    end

    Client -->|HTTP Request| Nginx
    Nginx -->|Proxy Pass| API
    API -->|1. Valida & Persiste| DB
    API -->|2. RPUSH Job ID| Redis
    API -.->|Guarda imagen| Volume
    Redis -->|3. BLPOP Bloqueante| Worker
    Worker -->|4. Lee & Procesa Chunks| Volume
    Worker -->|5. Actualiza % Progreso| Redis
    Worker -->|6. Guarda Resultado| Volume
    Client -.->|GET /jobs/id Polling| API
```

### ⚙️ Características Técnicas Principales
* **Desacoplamiento Total:** La API responde en milisegundos (`201 Created` con UUID) y delega la computación pesada a una cola en memoria.
* **Productor-Consumidor con Redis:** Utiliza `RPUSH` y `BLPOP` bloqueante para balanceo automático de carga sin consumo inútil de ciclos de CPU.
* **Paralelismo Real en CPU:** El *Worker* divide las matrices de imagen con **NumPy** en bloques (*chunks*) y utiliza `ProcessPoolExecutor` para evitar el GIL (Global Interpreter Lock) de Python, exprimiendo todos los núcleos del procesador.
* **Tracking de Progreso en Tiempo Real:** El estado de cada trabajo (`queued` ➔ `processing` ➔ `finished` / `failed`) y su porcentaje (`0%` a `100%`) se actualizan dinámicamente en Redis.
* **Persistencia Transaccional:** Registro permanente de metadatos en **MariaDB** mediante **SQLAlchemy**.
* **Seguridad y Proxy Inverso:** Enrutamiento a través de **NGINX**, cabeceras CORS habilitadas y autenticación HTTP Basic con contraseñas cifradas mediante Hashing (`Werkzeug`).

### ⚡ Cómo Ejecutarlo en 1 Comando
```bash
# Clonar el repositorio
git clone https://github.com/adriimaa/sd-pl2-g14.git
cd sd-pl2-g14/P5/compose-ej1

# Levantar los 5 contenedores orquestados
docker compose up --build
```
* Acceso a la interfaz web: `http://localhost:8080/static/main-auth.html`
* Credenciales de acceso: Usuario: `alumno` | Contraseña: `alumno_pass`

---

## 📂 Estructura de Módulos del Repositorio

| Módulo | Nombre / Ámbito | Tecnologías Clave | Resumen Técnico |
| :--- | :--- | :--- | :--- |
| **[P5](./P5)** | **Distributed Async Task Pipeline** | `Docker Compose`, `Redis`, `Flask`, `MariaDB`, `NumPy`, `Nginx` | **Proyecto Estrella.** Sistema productor-consumidor para procesamiento paralelo en clúster. |
| **[P4](./P4)** | **RESTful Engine & Persistencia** | `Flask`, `Gunicorn`, `MariaDB`, `SQLAlchemy`, `HATEOAS`, `Click` | API REST de nivel 3 de madurez (HATEOAS), autenticación con hashing, cliente CLI con librería `Click` y despliegue multi-worker en Gunicorn. |
| **[P3](./P3)** | **Web Scraping & Pipelines ETL** | `Scrapy`, `BeautifulSoup4`, `Requests`, `Pandas` | Extracción masiva de datos estructurados con XPath y selectores CSS en portales web (FilmAffinity, Federación Española de Baloncesto), exportando a CSV/Excel. |
| **[P2](./P2)** | **Peer-to-Peer Messaging System** | `Python Sockets`, `UDP`, `Redis`, `Select I/O Multiplexing` | Chat P2P descentralizado sin servidor central para mensajes, utilizando Redis como directorio dinámico de presencia y resolución de IPs. |
| **[P1](./P1)** | **Core Network Protocols & Concurrencia** | `Sockets UDP/TCP`, `Exponential Backoff`, `Broadcast`, `Fork` | Protocolo fiable de transporte sobre UDP con control de pérdidas, descubrimiento de servidores por Broadcast en red Docker, y servidores TCP concurrentes con hilos y procesos. |

---

## 📑 Memoria Técnica
El proyecto cuenta con una memoria académica y técnica completa de **79 páginas** donde se documentan paso a paso los experimentos de red, capturas de tráfico, pruebas de carga y métricas de rendimiento:
* 📥 [Descargar Memoria Técnica en PDF](./docs/Memoria_Sistemas_Distribuidos.pdf)

---

## 👤 Autores
* **Adrián Manso Martínez** - [GitHub @adriimaa](https://github.com/adriimaa)  
  *Grado en Ciencia e Ingeniería de Datos (Universidad de Oviedo) & DAM (Desarrollo de Aplicaciones Multiplataforma)*
* **Yonathan Patricio Torrejón Martínez**
