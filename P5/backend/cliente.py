import click
import requests

BASE_URL = "http://localhost/jobs"
AUTH = ('alumno', 'alumno_pass')

@click.group()
def cli():
    """
    Aplicación de filtros cliente.
    Utiliza comandos para interactuar con el servidor.
    """
    pass


@cli.command()
@click.argument("ruta")
@click.option("--filtro",default="grises")
def new(ruta, filtro):
    """
    Crea un nuevo trabajo.
    Uso: python cliente.py new "/ruta/tu_imagen.jpg/png" --filtro (sepia/grises/blur)
    """
    data = {
        "ruta": ruta,
        "filtro": filtro
    }
    response = requests.post(url=BASE_URL,json=data,auth=AUTH)
    if response.status_code == 201:
        data = response.json()
        job_id = data.get('job_id')
        print(f"   ID: {job_id}")
        print(f"   Estado: {data.get('status')}")
        print(f"   URI: {data.get('uri')}")
    elif response.status_code == 400:
        print(f"Error de solicitud: {response.json().get('error')}")
    else:
        print("Error en la peticion")


@cli.command()
@click.argument("job_id")
def status(job_id):
    """
    Consulta estado de un trabajo por su id
    Uso: python cliente.py status <ID>
    """
    url = f"{BASE_URL}/{job_id}"

    response = requests.get(url, auth=AUTH)

    if response.status_code == 200:
        data = response.json()
        estado = data.get('status')
        progreso = data.get('progress', '0')

        print(f"Trabajo -> {job_id}")
        print(f"Estado: {estado}")
        print(f"Progreso: {progreso}%")
        print(f"Ruta: {data.get('input_ruta')}")

        if estado == 'finished':
            res = data.get('result', {})
            print(f"Resultado: {res.get('archivo')}")
        elif estado == 'failed':
            print(f"Error: {data.get('error')}")

    elif response.status_code == 404:
        print("Trabajo no encontrado")
    else:
        print(f"Error en la peticion status")

@cli.command()
def list():
    """
    Todos los trabajos registrados en la base de datos.
    """
    url = BASE_URL
    response = requests.get(url, auth=AUTH)

    if response.status_code == 200:
        data = response.json()
        trabajos = data.get("trabajos", [])

        if not trabajos:
            print("No hay trabajos registrados.")
            return

        for t in trabajos:
            print(f"- ID: {t.get('job_id')}   Estado: {t.get('status')}   Filtro: {t.get('input_filtro')}  Ruta: {t.get('input_ruta')}" )

    else:
        print(f"Error al obtener la lista")

if __name__ == "__main__":
    cli()