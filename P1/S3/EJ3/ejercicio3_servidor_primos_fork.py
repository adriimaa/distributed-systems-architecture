import sys
import socket
import time
import os

def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        time.sleep(0.1)
        if numero % i == 0:
            return False
    return True

def calcular_cliente(num_proceso, cliente_socket, cliente_address):
    print("Soy el proceso %i" % num_proceso)
    # COMPLETAR
    # Misma idea que en la ejecución secuencial, es decir:
    # Recibir la cantidad de primos a calcular
    data = cliente_socket.recv(1024).decode()
    numero = int(data)

    # Enviar un mensaje al cliente por cada 5 números calculados
    primos = []
    candidato = 2
    while len(primos) < numero:
        if es_primo(candidato):
            primos.append(candidato)

        if len(primos) % 5 == 0 and len(primos) != numero:
            mensaje = "Se han calculado %i de los %i números primos solicitados\n" % (len(primos), numero)
            cliente_socket.sendall(mensaje.encode())
        candidato += 1
    # Enviar la lista completa tras procesar la cantidad solicitada
    mensaje = "Primos:" + str(primos)
    cliente_socket.sendall(mensaje.encode())
    
    # Enviar "FIN" y cerrar el socket
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()
    print("Conexión cerrada con:", cliente_address)
    

# Proceso principal
if len(sys.argv) != 2:
    print("Uso: servidor.py puerto")
    sys.exit(1)

puerto_servidor = sys.argv[1]

# Crear el socket TCP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al puerto especificado
servidor_socket.bind(('', int(puerto_servidor)))

# Escuchar por conexiones entrantes
servidor_socket.listen(4)


print("El servidor está listo para recibir conexiones")
num_proceso = 0

while True:
    # Esperar a que llegue una conexión
    print("- Proceso principal esperando cliente -")
    cliente_socket, cliente_address = servidor_socket.accept()
    print("Conexión establecida desde:", cliente_address)

    pid = os.fork()
    
    if pid == 0:
        servidor_socket.close()
        calcular_cliente(num_proceso, cliente_socket, cliente_address)
        sys.exit(0)
    else:
        cliente_socket.close()    
        num_proceso += 1
    