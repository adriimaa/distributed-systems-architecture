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

while mensaje != b"":
    enviados = s.send(mensaje)
    mensaje=mensaje[enviados:]
  
mensaje_final = "FINAL"
print(f"Enviando: '{mensaje_final}'")
s.sendall(mensaje_final.encode("ascii"))

s.close()
print("Socket cerrado. Terminando cliente.")