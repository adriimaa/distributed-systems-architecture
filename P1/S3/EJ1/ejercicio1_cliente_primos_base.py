import sys
import socket
import datetime

if len(sys.argv) != 4:
    print("Uso: cliente.py ip puerto cantidadPrimos")
    sys.exit(1)

ip_servidor = sys.argv[1]
puerto_servidor = sys.argv[2]
cantidad = int(sys.argv[3])

# Crear el socket TCP
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
cliente_socket.connect((ip_servidor, int(puerto_servidor)))

# Enviar el número al servidor
cliente_socket.sendall(str(cantidad).encode())

# Recibir y mostrar los mensajes del servidor
while True:
    data = cliente_socket.recv(1024).decode()
    if data:
        hora_actual = datetime.datetime.now().time()
        print("La hora actual es:", hora_actual)
        print(data)

    # Si se ha recibido "FIN", salir del bucle
    if "FIN" in data:
        cliente_socket.close()
        break