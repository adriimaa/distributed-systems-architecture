import sys
import select
import socket
import redis


if len(sys.argv) != 3:
    print("Uso: python3 ejercicio2_borrar_nick_redis.py <nombre> <ip_redis>")
    sys.exit(1)

ip_redis = sys.argv[2]
nombre = sys.argv[1]
puerto = 6379


#Crear instancia redis
redis_client = redis.Redis(host=ip_redis, port=puerto, db=0)

num_eliminadas = redis_client.delete(nombre)

if num_eliminadas == 1:
    print(f"La clave ha sido eliminada")
else:
    print("La clave no existia")    

sys.exit(0)



