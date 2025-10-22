# ejercicio3_servidor_primos_fork.py
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

#Sustituimos los hilos por procesos.
def calcular_cliente(num_proceso, cliente_socket, cliente_address):
    print("Soy el proceso %i (PID: %i)" % (num_proceso, os.getpid()))
    
    # Recibir la cantidad de primos a calcular
    data = cliente_socket.recv(1024).decode()
    numero = int(data)
    print("Calculando los primeros %i números primos para el proceso %i..." % (numero, num_proceso))

    # Calcular los números primos
    primos = []
    candidato = 2
    while len(primos) < numero:
        if es_primo(candidato):
            primos.append(candidato)

            if len(primos) % 5 == 0 and len(primos) != numero:
                mensaje = "Se han calculado %i de los %i números primos solicitados\n" % (len(primos), numero)
                cliente_socket.sendall(mensaje.encode())
        
        candidato += 1

    # Enviar la lista completa
    mensaje = "Primos:" + str(primos)
    cliente_socket.sendall(mensaje.encode())

    # Enviar "FIN" para indicar el final y cerrar el socket
    cliente_socket.sendall("FIN".encode())
    cliente_socket.close()
    print("Proceso %i completado. Conexión cerrada con: %s" % (num_proceso, cliente_address))

if len(sys.argv) != 2:
    print("Uso: servidor.py puerto")
    sys.exit(1)

puerto_servidor = int(sys.argv[1])

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor_socket.bind(('', puerto_servidor))

servidor_socket.listen(4)

print("El servidor está listo para recibir conexiones")
num_proceso = 0

while True:
    # Esperar a que llegue una conexión
    print("- Proceso padre esperando cliente -")
    cliente_socket, cliente_address = servidor_socket.accept()
    print("Conexión establecida desde:", cliente_address)

    # Crear un proceso hijo 
    pid = os.fork()
    
    if pid == 0:
        # Proceso hijo
        servidor_socket.close()
        calcular_cliente(num_proceso, cliente_socket, cliente_address)
        sys.exit()  # Finaliza el proceso hijo
    else:
        # Proceso padre
        cliente_socket.close()
