import socket

PUERTO = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Activamos el modo broadcast para el socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(("", PUERTO))
print(f"Servidor Broadcast 'HOLA' escuchando en el puerto {PUERTO}")

while True:
    mensaje_bytes,dir_cliente = sock.recvfrom(1024)
    mensaje = mensaje_bytes.decode("utf-8")

    print(f"Recibido '{mensaje}' de {dir_cliente}")

    if mensaje == "BUSCANDO HOLA":
        # Respondemos que implementamos el servicio
        sock.sendto(b"IMPLEMENTO HOLA", dir_cliente)
        
    elif mensaje == "HOLA":
        # Ofrecemos el servicio
        ip_cliente = dir_cliente[0]
        respuesta = f"HOLA: {ip_cliente}"
        sock.sendto(respuesta.encode("utf-8"), dir_cliente)