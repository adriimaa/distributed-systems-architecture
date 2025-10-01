import socket
import sys
import random

if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])
else:
    PUERTO = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PUERTO))
print(f"Servidor UDP (con OK) escuchando en el puerto {PUERTO}")

while True:
    mensaje_bytes, direccion_cliente = sock.recvfrom(1024)

    if random.randint(0, 1) == 0:
        print(f"Simulando paquete perdido desde {direccion_cliente}")
        continue

    mensaje = mensaje_bytes.decode("utf-8")
    print(f"Mensaje recibido de {direccion_cliente}: {mensaje}")
   
    # Enviamos la confirmación "OK" al cliente.
    sock.sendto(b"OK", direccion_cliente) 