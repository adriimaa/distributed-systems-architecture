import random
import socket
import sys

if len(sys.argv) > 1:
    puerto= int(sys.argv[1])
else:
    puerto = 9999
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",puerto))
print(f"Servidor UDP (simula perdidas) escuchando en el puerto {puerto}")

while True:
    mensaje,dir = sock.recvfrom(1024)
    
    if random.randint(0,1) == 0:
        print(f"Simulando paquete perdido desde {dir}")
        continue
    mensaje = mensaje.decode("utf-8")
    print(f"Mensaje recibido de {dir}: {mensaje}")