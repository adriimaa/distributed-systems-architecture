import socket
import sys

if len(sys.argv) > 2:
    IP_SERVIDOR = sys.argv[1]
    PUERTO_SERVIDOR = int(sys.argv[2])
else:
    IP_SERVIDOR = "localhost"
    PUERTO_SERVIDOR = 9999

dir_servidor = (IP_SERVIDOR, PUERTO_SERVIDOR)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
num = 1

while True:
    mensaje_usuario = input("Introduce un mensaje para enviar (o 'FIN' para terminar): ")
    if mensaje_usuario == "FIN":
        break

    mensaje_secuencia = f"{num}, {mensaje_usuario}"

    confi_recibida = False
    timeout_inicial = 0.1

    #Bucle

    while not confi_recibida and timeout_inicial <= 2.0:
        print(f"Enviando (intento con timeout={timeout_inicial}s): '{mensaje_secuencia}'")
        sock.sendto(mensaje_secuencia.encode("utf-8"), dir_servidor)

        sock.settimeout(timeout_inicial)

        try:
            respuesta_bytes, _ = sock.recvfrom(1024)
            if respuesta_bytes.decode("utf-8") == "OK":
                print("Recibida confirmación 'OK' del servidor.")
                confirmacion_recibida = True
        except socket.timeout:
            print("Timeout. Reintentando...")
            timeout_inicial *= 2

    if not confi_recibida:
        print("Puede q el server este caido, Intentelo mas tarde")
        break
    num += 1

print("Cerrando al cliente.")
sock.close()

