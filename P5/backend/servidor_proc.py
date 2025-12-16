import time
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os
import redis
import json
import threading

#Variables redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

#Funciones para aplicar filtros 3 tipos l13 progr avanzada
def aplicar_escala_grises(chunk):
    """Convierte un chunk de imagen a escala de grises"""
    alto, ancho = chunk.shape[0], chunk.shape[1]
    resultado = chunk.copy()

    # Procesar píxel por píxel
    for i in range(alto):
        for j in range(ancho):
            r, g, b = int(chunk[i, j, 0]), int(chunk[i, j, 1]), int(chunk[i, j, 2])
            # Fórmula estándar de luminancia
            gris = int(r * 0.299 + g * 0.587 + b * 0.114)
            resultado[i, j, 0] = gris
            resultado[i, j, 1] = gris
            resultado[i, j, 2] = gris

    return resultado.astype(np.uint8)


def aplicar_blur(chunk, kernel_size=5):
    """Aplica un filtro de blur simple """
    alto, ancho = chunk.shape[0], chunk.shape[1]
    resultado = chunk.copy()
    radio = kernel_size // 2
    time.sleep(5)

    # Blur simple:
    for i in range(radio, alto - radio):
        for j in range(radio, ancho - radio):
            # Calcular promedio de ventana para cada canal
            for canal in range(3):  # R, G, B
                suma = 0
                count = 0
                for di in range(-radio, radio + 1):
                    for dj in range(-radio, radio + 1):
                        suma += int(chunk[i + di, j + dj, canal])
                        count += 1
                resultado[i, j, canal] = suma // count

    return resultado.astype(np.uint8)


def aplicar_sepia(chunk):
    """Aplica efecto sepia """
    alto, ancho = chunk.shape[0], chunk.shape[1]
    resultado = chunk.copy()

    # Procesar píxel por píxel con matriz sepia
    for i in range(alto):
        for j in range(ancho):
            r, g, b = int(chunk[i, j, 0]), int(chunk[i, j, 1]), int(chunk[i, j, 2])

            # Aplicar matriz sepia
            nuevo_r = int(r * 0.393 + g * 0.769 + b * 0.189)
            nuevo_g = int(r * 0.349 + g * 0.686 + b * 0.168)
            nuevo_b = int(r * 0.272 + g * 0.534 + b * 0.131)

            # Limitar a rango 0-255
            resultado[i, j, 0] = min(255, nuevo_r)
            resultado[i, j, 1] = min(255, nuevo_g)
            resultado[i, j, 2] = min(255, nuevo_b)

    return resultado.astype(np.uint8)


def procesar_chunk(args):
    """
    Procesa un chunk de imagen aplicando el filtro especificado.
    """
    chunk_data, filtro, numero_chunk = args

    # Aplicar el filtro correspondiente
    if filtro == 'grises':
        chunk_procesado = aplicar_escala_grises(chunk_data)
    elif filtro == 'blur':
        chunk_procesado = aplicar_blur(chunk_data)
    elif filtro == 'sepia':
        chunk_procesado = aplicar_sepia(chunk_data)
    else:
        raise ValueError(f"Filtro no soportado: {filtro}")

    return (numero_chunk, chunk_procesado)


#FUNCIONES AUXILIARES

#funcion pl13 progr avanzada
def cargar_imagen(ruta):
    """Carga la imagen y la convierte a RGB para evitar errores con PNGs"""
    if not ruta or not os.path.exists(ruta):
        return None
    try:
        imagen = Image.open(ruta).convert('RGB')
        return np.array(imagen)
    except Exception as e:
        print(f"Error cargando imagen: {e}")
        return None


#Guardar imagen en static para verla desde el main-auth.html
def guardar_resultado(resultado_final, ruta_original, filtro, job_id):
    """Guarda la imagen en la carpeta static"""

    if ruta_original:
        # Extrae foto
        base = os.path.splitext(os.path.basename(ruta_original))[0]
        # Extrae ruta
        ext = os.path.splitext(os.path.basename(ruta_original))[1]

        nombre_archivo = f"{base}_{filtro}{ext}"
    else:
        nombre_archivo = f"procesada_{job_id}_{filtro}.jpg"

    if not os.path.exists("static"):
        os.makedirs("static")

    # la guarda
    ruta_salida = os.path.join("static", nombre_archivo)
    Image.fromarray(resultado_final).save(ruta_salida)

    return nombre_archivo

#Lógica principal servidor (paralelismo práctica 13-Programación Avanzada)pero utilizando Redis
def ejecutar_trabajo(job_id):

    print(f"Iniciando trabajo {job_id}")

    # Actualizamos estado redis a procesando
    redis_client.set(f"{job_id}:status", "processing")
    redis_client.set(f"{job_id}:progress", "0")

    try:

        ruta_imagen = redis_client.get(f"{job_id}:input_ruta").decode('utf-8')
        filtro = redis_client.get(f"{job_id}:input_filtro").decode('utf-8')

        #Cargar imagen
        imagen_array = cargar_imagen(ruta_imagen)
        if imagen_array is None:
            raise FileNotFoundError(f"La imagen no existe o no se puede leer: {ruta_imagen}")

        # Paralelismo
        num_cpus = multiprocessing.cpu_count()
        num_chunks = min(num_cpus, 8)

        chunks = np.array_split(imagen_array, num_chunks, axis=0)
        args_list = [(chunk, filtro, i) for i, chunk in enumerate(chunks)]

        resultados = []
        completados = 0

        # PocessPool (PL13)
        with ProcessPoolExecutor(max_workers=num_chunks) as executor:

            future_to_chunk = {
                executor.submit(procesar_chunk, args): args[2]
                for args in args_list
            }

            for future in as_completed(future_to_chunk):
                chunk_num = future_to_chunk[future]
                try:
                    resultado = future.result()
                    resultados.append(resultado)
                    completados += 1

                    # se guarda el progreso por cada chunk procesado
                    progreso = int((completados / num_chunks) * 100)

                    # Estruturaa set redis actualizamos progreso poco a poco
                    redis_client.set(f"{job_id}:progress", str(progreso))
                    print(f"Job {job_id}: Progreso {progreso}%")
                    time.sleep(5)

                except Exception as e:
                    print(f"Error en chunk {chunk_num}: {e}")

        #Ordenar y Guardar
        resultados.sort(key=lambda x: x[0])
        chunks_procesados = [chunk for _, chunk in resultados]
        resultado_final = np.vstack(chunks_procesados)

        nombre = guardar_resultado(resultado_final, ruta_imagen, filtro, job_id)

        #Finalizar trabajo en Redis
        # Guardamos el nombre del fichero generado

        lista = [nombre,"Procesado correctamente"]
        resultado = ";".join(map(str, lista))

        #actualizamos redis
        redis_client.set(f"{job_id}:result", resultado)
        redis_client.set(f"{job_id}:progress", "100")
        redis_client.set(f"{job_id}:status", "finished")

        print(f"Trabajo {job_id} FINALIZADO")

    except Exception as e:
        print(f"Error procesando trabajo {job_id}: {e}")
        redis_client.set(f"{job_id}:status", "failed")
