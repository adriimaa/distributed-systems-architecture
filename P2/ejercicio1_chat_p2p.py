import sys
import select
import socket

if len(sys.argv) != 3:
    print("Uso: python3 ejercicio1_chat_p2p.py <puerto> <nombre>")
    sys.exit(1)

puerto = int(sys.argv[1])
nombre = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.bind(("",puerto))
print(f"Cliente de chat iniciado. Escuchando en puerto {puerto}")
print(f"Tu nombre es: {nombre}")

destino_chat = None

#Pseudocodigo

#Bucle infinito
while True:
    #imprimir el prompt
    print("> ", end="",)
    #esperar con select()
    listo, _, _ = select.select([s, sys.stdin.fileno()], [], [])
    #Si hay datos en el socket
    if s in listo:
        #Leemos e imprimimos
        datos,direccion = s.recvfrom(1024)
        mensaje = datos.decode('utf-8')
        print(f"{mensaje}")
        print("> ",end="")
    #Si hay datos en el teclado
    if sys.stdin.fileno() in listo:
        #Leemos
        linea=input().strip

        #Procesar la linea segun su contenido
        if linea.starswith("/QUIT"):

