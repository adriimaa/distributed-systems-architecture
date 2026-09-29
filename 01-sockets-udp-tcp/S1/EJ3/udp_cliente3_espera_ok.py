import socket
import sys

if len(sys.argv) > 2:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = int(sys.argv[2])
else:
    IP_SERVIDOR = "localhost"
    PUERTO_SERVIDOR = 9999

direccion_servidor = (IP_SERVIDOR, PUERTO_SERVIDOR)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
numero_secuencia = 1

while True:
    mensaje_usuario = input("Introduce un mensaje para enviar (o 'FIN' para terminar): ")
    if mensaje_usuario == "FIN":
        break

    mensaje_con_secuencia = f"{numero_secuencia}: {mensaje_usuario}"
   
    print(f"Enviando: '{mensaje_con_secuencia}'")
    sock.sendto(mensaje_con_secuencia.encode("utf-8"), direccion_servidor)
   
    # tiempo
    sock.settimeout(0.5) # 0.5 segundos

    try:
        # Esperamos la confirmación del servidor
        respuesta_bytes, _ = sock.recvfrom(1024)
        if respuesta_bytes.decode("utf-8") == "OK":
            print("Recibida confirmación 'OK' del servidor.")
        else:
            print("Respuesta inesperada del servidor.") 
    except socket.timeout:
        print("ERROR: No se recibió confirmación del servidor (timeout).")
   
    numero_secuencia += 1

print("Cerrando el cliente.")
sock.close()