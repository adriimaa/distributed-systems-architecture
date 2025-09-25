# PROCESO 1
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

direccion_servidor = ("82.2.5.23", 9999)                                

# Enviamos 5 mensajes, esperamos sus respuestas, y las imprimimos
for i in range(5):
    mensaje = f'Mensaje {i}'
    sock.sendto(mensaje.encode("utf-8"), direccion_servidor)            
    respuesta, _ = sock.recvfrom(1024)                                  
    print(f'Respuesta recibida: {respuesta.decode("utf-8")}')
