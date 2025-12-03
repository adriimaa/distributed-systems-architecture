#!/bin/bash

# Detener los tres contenedores
echo "Deteniendo nginx_tarea..."
docker stop nginx_tarea
echo "Deteniendo tarea_app_flask..."
docker stop tarea_app_flask
echo "Deteniendo mariadb_tarea_db..."
docker stop mariadb_tarea_db

# Esperar unos segundos para asegurarnos de que los contenedores se detengan correctamente
echo "Esperando 10 segundos..."
sleep 10

# Eliminar los contenedores detenidos
echo "Eliminando contenedores detenidos..."
docker container prune -f

# Esperar 5 segundos para asegurarnos de que los contenedores eliminados se liberen correctamente
COMPLETAR

# Volver a lanzar los tres contenedores
echo "Lanzando contenedor con la BBDD..."
docker run COMPLETAR

# Esperar 5 segundos para asegurarnos de que la base de datos esté en funcionamiento antes de lanzar la aplicación Flask
COMPLETAR
echo "Lanzando contenedor con la aplicación FLASK..."
docker run COMPLETAR

# Esperar 2 segundos para lanzar el último contenedor (nginx)
COMPLETAR
echo "Lanzando contenedor con el proxy NGINX..."
docker run COMPLETAR

echo "Ejecutando docker ps..."
docker ps