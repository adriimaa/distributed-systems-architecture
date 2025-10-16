import socket 
import sys
import time

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
    
    time.sleep(1)
    f=sd.makefile(encoding="utf-8",newline="\r\n")
    
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        mensaje = f.readline()
        
        if not mensaje:
            print("Conexión cerrada por el cliente.")
            sd.close()
            continuar = False
        else:
            # Le quitamos el delimitador "\r\n"
            linea = mensaje[:-2]
            # Invertimos la línea.
            linea_invertida = linea[::-1]
            
            # Preparamos la respuesta añadiendo el delimitador.
            respuesta = linea_invertida + "\r\n"
            sd.sendall(respuesta.encode("utf-8"))
        
f.close()
sd.close()
print("Socket cerrado")
