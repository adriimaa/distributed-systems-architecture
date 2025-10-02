import socket 
import sys

# Se añade la función recvall
def recvall(sock, num_bytes):
    """
    Función que recibe exactamente num_bytes de un socket.
    Usa un bucle para asegurar que se leen todos los datos solicitados.
    """
    chunks = []
    bytes_recibidos = 0
    while bytes_recibidos < num_bytes:
        chunk = sock.recv(num_bytes - bytes_recibidos)
        if chunk == b'':
            raise RuntimeError("Conexión del socket rota")
        chunks.append(chunk)
        bytes_recibidos = bytes_recibidos + len(chunk)
    
    return b''.join(chunks).decode('ascii')

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor TCP (con recvall) escuchando en {puerto}")

# Bucle
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = sd.recv(5)  # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii")  # Pasar los bytes a caracteres
                # En este ejemplo se asume que el texto recibido es ascii puro
        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)

