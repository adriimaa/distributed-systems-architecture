import socket 
import sys

IP = "255.255.255.255"
PUERTO = 12345

if len(sys.argv) > 2:
    IP = sys.argv[1]
    PUERTO = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Activamos el modo broadcast para poder enviar.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"Buscando servidores 'HOLA' en {IP}:{PUERTO}...")
sock.sendto(b"BUSCANDO HOLA", (IP, PUERTO))

sock.settimeout(2.0)
servidores = []

try:
    while True:
        respuesta_bytes, dir_servidor = sock.recvfrom(1024)

        if respuesta_bytes == b"IMPLEMENTO HOLA":
            print(f"Servidor encontrado en: {dir_servidor}")
            servidores.append(dir_servidor)
except socket.timeout:
    print("Fin de la búsqueda de servidores.")

if servidores:
    servidor1 = servidores[0]
    print(f"\nUsando el servicio del primer servidor: {servidor1}")

    sock.settimeout(None)

    sock.sendto(b"HOLA",servidor1)
    respuesta, _ = sock.recvfrom(1024)
    print(f"Respuesta del servidor: {respuesta.decode('utf-8')}")
else:
    print("\n No se encontraron servers 'HOLA' ")

sock.close()
