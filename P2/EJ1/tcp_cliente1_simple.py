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


mensaje = b"ABCDE"
# Enviar los 5 bytes en tantas veces como sea necesario
while mensaje != b"":
    enviados = s.send(mensaje)
    mensaje=mensaje[enviados:]    # Reasignar los restantes

print(f"{mensaje}")

s.close()
print("Socket cerrado. Terminando cliente.")