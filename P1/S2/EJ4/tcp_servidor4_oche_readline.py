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
    f=sd.makefile(mode="rw",encoding="utf-8",newline="\r\n")
    
    while True:
        linea = f.readline()
        print(f"Recibido:{repr(linea)}")
        
        if not linea:
            print("Conexión cerrada por el cliente.")
            break
        
        linea_sin_salto=linea.strip()
        linea_invertida=linea_sin_salto[::-1]
        
        respuesta=linea_invertida
        print(f"Enviando:{repr(respuesta+f.newlines)}")
        f.write(respuesta+f.newlines)
        
f.close()
sd.close()
print("Socket cerrado")
