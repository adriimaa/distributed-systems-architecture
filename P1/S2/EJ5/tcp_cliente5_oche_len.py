import socket
import sys

def recvall(sock, num_bytes):
    
    datos_recibidos =b"" 
    while len(datos_recibidos) < num_bytes:
        fragmento = sock.recv(num_bytes- len(datos_recibidos))
        if not fragmento:
            return None
        datos_recibidos+=fragmento
    return datos_recibidos

def recibe_longitud(sd):

    long = b""
    while True:
        byte = sd.recv(1)
        if byte == b"\n":
            break
        if not byte:
            return None
        long += byte

    return int(long.decode("utf-8"))

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
    
    longitud_msg  = "%d\n" % len(bytes(msg, "utf8"))
    s.sendall(bytes(longitud_msg + msg, "utf8"))

    # Recibimos la respuesta
    longitud = recibe_longitud(s)
    mensaje = s.recvall(longitud)
    mensaje = mensaje.decode("utf-8")
    print(f"Recibido: {repr(mensaje)}")
    
s.close()
print("Socket cerrado")