import socket
import sys

def main():
	port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	direccion_servidor = (" ", 9999)

	server_socket.bind(('', port))
        print(f"Server listening on port {port}...")

	# Bucle infinito 
	while True:
		data,adress = server_socket.recvfrom(1024)
		print(f"Mensaje recibido: '{data.decode{}' from {adress}")

	server_socket.close()
