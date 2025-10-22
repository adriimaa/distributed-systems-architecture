import sys
import select
import socket

if len(sys.argv) != 3:
    print("Uso: python3 ejercicio1_chat_p2p.py <puerto> <nombre>")
    sys.exit(1)

puerto = int(sys.argv[1])
nombre = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)