 import socket

 cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 sock.bind(("82.2.5.23", 9999))

 while True:
	message = "da"
	# Get input from the user
        message = input("> ")

        # If the user types 'FIN', break the loop
        if message == "FIN":
            break

        # Send the message to the server
            client_socket.sendto(message.encode(), server_address)

socket.close()
