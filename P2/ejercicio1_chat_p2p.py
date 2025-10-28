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
        linea=sys.stdin.readline().strip()

        #Procesar la linea segun su contenido
        if linea.startswith("/QUIT"):
            print("Cerrando cliente")
            s.close()
            sys.exit(0)
        elif linea.startswith("/CHAT"):
            partes = linea.split()
            if len(partes) == 3 and partes[2].isdigit():
                ip_destino = partes[1]
                puerto_destino = int(partes[2])
                destino_chat = (ip_destino, puerto_destino)
            else:
                print("Uso: /CHAT <ip> <puerto>")
        elif linea:
            if destino_chat is None:
                print("Antes debes hacer /CHAT <ip> <puerto>")
            else:
                s.sendto(f"{nombre}: {linea}".encode('utf-8'), destino_chat)
                
