import socket
import sys

if len(sys.argv) > 2:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = int.argv[2]
else:
    IP_SERVIDOR = "localhost"
    PUERTO_SERVIDOR = 9999

dir_servidor = (IP_SERVIDOR, PUERTO_SERVIDOR)

#Creamos el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bucle para leer texto del teclado y enviarlo.
while True:
    mensaje = input("Introduce un mensaje para enviar (o 'FIN' para terminar): ")
    if mensaje == "FIN":
        break

    sock.sendto(mensaje.encode("utf-8"), dir_servidor)

print("Cerrando cliente...")
sock.close()
