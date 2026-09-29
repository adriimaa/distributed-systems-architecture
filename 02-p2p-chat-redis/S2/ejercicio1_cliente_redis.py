import sys
import select
import socket
import redis


#Sin usar bibliotecas adicionales
def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  # 8.8.8.8 es una IP externa válida
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local


if len(sys.argv) != 3:
    print("Uso: python3 ejercicio1_cliente_redis.py <nombre> <ip_redis>")
    sys.exit(1)

ip_redis = sys.argv[2]
nombre = sys.argv[1]
puerto = 6379

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.bind(("",0))

mi_ip = obtener_ip_local()
mi_puerto = s.getsockname()[1]

print(f"Cliente de chat iniciado. Escuchando en{mi_ip}:{mi_puerto}")
print(f"Tu nombre es: {nombre}")

#Crear instancia redis
redis_client = redis.Redis(host=ip_redis, port=puerto, db=0)

if redis_client.exists(nombre):
    print("Ya esta en uso")
    s.close()
    sys.exit(1)

ip_puerto = f"{mi_ip}:{mi_puerto}"
redis_client.set(nombre, ip_puerto)

destino_chat = None

#Pseudocodigo

#Bucle infinito
while True:
    #imprimir el prompt
    print("> ", end="",)
    #esperar con select()
    listo, _, _ = select.select([s, sys.stdin.fileno()], [], [])
    #Si hay datos en el socket
    if s in listo:
        #Leemos e imprimimos
        datos,direccion = s.recvfrom(1024)
        mensaje = datos.decode('utf-8')
        print(f"{mensaje}")
        print("> ",end="")
    #Si hay datos en el teclado
    if sys.stdin.fileno() in listo:
        #Leemos
        linea=sys.stdin.readline().strip()

        #Procesar la linea segun su contenido
        if linea.startswith("/QUIT"):
            print("Cerrando cliente")
            redis_client.delete(nombre)
            s.close()
            sys.exit(0)
        elif linea.startswith("/CHAT"):
            partes = linea.split()
            if len(partes) == 2:
                nombre_destino = partes[1]
                valor = redis_client.get(nombre_destino)

                if valor is None:
                    print(f"Error: El usuario '{nombre_destino}' no está registrado.")
                    destino_chat = None
                else:
                    valor_str = valor.decode('utf-8')
                    ip_destino, puerto_str = valor_str.split(':')
                    puerto_destino = int(puerto_str)
                    destino_chat = (ip_destino, puerto_destino)
                    print(f"Hablando con {nombre_destino}:")
            else:
                print("Uso: /CHAT <nombre>")
        elif linea:
            if destino_chat is None:
                print("Antes debes hacer /CHAT <nombre>")
            else:
                s.sendto(f"{nombre}: {linea}".encode('utf-8'), destino_chat)