import socket
import sys

if len(sys.argv) > 2:
    ip_servidor = sys.argv[1]
    puerto_servidor = int(sys.argv[2])
else:
    ip_servidor = "localhost"
    puerto_servidor = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip_servidor, puerto_servidor))
print(f"Conectado al servidor en {ip_servidor}, {puerto_servidor}")

mensajes = ["Hola", "Mundo", "Sistemas Distribuidos"]

for msg in mensajes:
    # Añadimos el delimitador \r\n
    mensaje_a_enviar = msg + "\r\n"
    print(repr(mensaje_a_enviar))
    s.sendall(bytes(mensaje_a_enviar, "utf8"))

    # Recibimos la respuesta
    respuesta = s.recv(80)
    print(f"Recibido: {repr(respuesta)}")

s.close()
print("Socket cerrado")