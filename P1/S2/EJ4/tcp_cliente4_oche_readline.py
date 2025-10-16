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

f = s.makefile(mode='rw', encoding='utf-8', newline='\r\n')

mensajes = ["Hola", "Mundo", "Sistemas Distribuidos"]

for msg in mensajes:
    # Añadimos el delimitador \r\n
    mensaje_a_enviar = msg + "\r\n"
    
    print(repr(mensaje_a_enviar))
    f.write(mensaje_a_enviar)

    # Recibimos la respuesta
    respuesta = f.readline()
    print(f"Recibido: {repr(respuesta)}")

f.close()
s.close()
print("Socket cerrado")