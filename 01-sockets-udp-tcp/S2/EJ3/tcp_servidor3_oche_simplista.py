import socket 
import sys

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("", puerto))
s.listen(5)

print(f"Servidor OCHE escuchando en el puerto {puerto}")

#Bucle
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos_bytes = sd.recv(80)
        
        if not datos_bytes:
            print("Conexión cerrada por el cliente.")
            continuar = False
        else:
            mensaje = datos_bytes.decode("utf-8")
            # Le quitamos el delimitador "\r\n"
            linea = mensaje[:-2]
            # Invertimos la línea.
            linea_invertida = linea[::-1]
            # Preparamos la respuesta añadiendo el delimitador.
            respuesta = linea_invertida + "\r\n"
            
            sd.sendall(respuesta.encode("utf-8"))

    sd.close()
    print("Socket cerrado")
