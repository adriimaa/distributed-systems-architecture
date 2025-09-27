import socket
import sys

#Puerto q se indique por linea de comandos o 9999 por defecto.
if len(sys.argv) > 1:
	puerto=int(sys.argv[1])
else:
	puerto = 9999

#cREAR SOCKET UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Asigno dir y puerto
sock.bind(("",puerto))
print(f"Servidor UDP escuchando en el puerto {puerto}")

#Bucle infinito:
while True:
	mensaje,dir=sock.recvfrom(1024)
	mensaje = mensaje.decode("uft-8")

	print(f"Mensaje recibido de {dir}: {mensaje}")

sock.close()