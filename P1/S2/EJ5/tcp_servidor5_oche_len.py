import socket
import sys

# Se añade la función recvall
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

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)
print(f"Servidor OCHE escuchando en el puerto {puerto}")

# Bucle
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado ")

    while True:
        longitud = recibe_longitud(sd)
        if longitud is None:
            print("Conexión cerrada por el cliente.")
            break

        mensaje = recvall(sd, longitud)
        if mensaje is None:
            print("Conexión cerrada inesperadamente por el cliente.")
            break
        
        print(f"Recibido ({longitud} bytes): {mensaje.decode('utf-8')}")
        
        mensaje_invertido_bytes = mensaje[::-1]

        longitud_respuesta = "%d\n" % len(mensaje_invertido_bytes)
        
        sd.sendall(bytes(longitud_respuesta, "utf-8") +mensaje_invertido_bytes)
        print(f"Respuesta enviada (con longitud: {len(mensaje_invertido_bytes)})")

            
    sd.close()
    print("Socket de datos cerrado.")