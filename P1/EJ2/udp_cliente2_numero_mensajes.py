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

num = 1

#Bucle para leer texto del teclado y enviarlo.
while True:
    mensaje_user = input("Introduce un mensaje para enviar (o 'FIN' para terminar): ")
    if mensaje_user == "FIN":
        break

    mensaje_secuencia = f"{num}: {mensaje_user}"

    print(f"Enviando: '{mensaje_secuencia}'")
    sock.sendto(mensaje_secuencia.encode("uft-8"), dir_servidor)

    num += 1

print("Cerrando cliente...")
sock.close()