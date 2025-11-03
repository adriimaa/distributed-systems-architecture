import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = f"https://www.primerafeb.com/estadisticas.aspx"

resultadoWeb = requests.get(url)
soup = BeautifulSoup(resultadoWeb.text, "html.parser")

#print(soup.prettify())

#Obtenemos las dos tablas con etiqueta 'tabla-estadistica'
tablas = soup.find_all("table", class_="tabla-estadistica")

#Separamos las tablas con sus repectivos datos
medias_equipo = tablas[0]
totales_equipo = tablas[1]

datos_medias = []
datos_totales = []

filas_tabla_medias = medias_equipo.find_all("tr")

for fila in filas_tabla_medias:
    
    celda_equipo = fila.find("td", class_="equipo")
    
    if celda_equipo:
        # Nombre del Equipo
        nombre_equipo = celda_equipo.text.strip()

        #Puntos
        puntos = fila.find("td", class_="puntos").text.strip()
        
        # Asistencias
        asistencias = fila.find("td", class_="asistencias").text.strip()

        #Valoracion
        valoracion = fila.find("td", class_="valoracion").text.strip()

        datos_medias.append({"Nombre": nombre_equipo,"Puntos": puntos, "Asistencia": asistencias,"Valoracion": valoracion})

#Ahora la otra tabla,puntos totales por equipo

filas_tabla_totales = totales_equipo.find_all("tr")

for fila in filas_tabla_totales:
    
    celda_equipo = fila.find("td", class_="equipo")
    
    if celda_equipo:
        # Nombre del Equipo
        nombre_equipo = celda_equipo.text.strip()

        #Puntos
        puntos = fila.find("td", class_="puntos").text.strip()
        
        # Asistencias
        asistencias = fila.find("td", class_="asistencias").text.strip()

        #Valoracion
        valoracion = fila.find("td", class_="valoracion").text.strip()

        datos_totales.append({"Nombre": nombre_equipo,"Puntos": puntos, "Asistencia": asistencias,"Valoracion": valoracion})

#Obtenemos csv, excel, json de la tabla medias por qeuipo
datos_medias_df = pd.DataFrame(datos_medias)

print(datos_medias_df.head(5))

datos_medias_df.to_csv('Medias_Equipo.csv', index=True)
print('CSV creado correctamente')

datos_medias_df.to_excel('Medias_Equipo.xlsx', index=False)
print('Excel creado correctamente: estadisticas_feb.xlsx')

datos_medias_df.to_json('Medias_Equipo.json', orient='records')
print('JSON creado correctamente')

#Obtenemos csv, excel, json de la tabla total puntos por equipo

datos_totales_df = pd.DataFrame(datos_totales)

print(datos_totales_df.head(5))

datos_totales_df.to_csv('Totales_Equipo.csv', index=True)
print('CSV creado correctamente')

datos_totales_df.to_excel('Totales_Equipo.xlsx', index=False)
print('Excel creado correctamente: estadisticas_feb.xlsx')

datos_totales_df.to_json('Totales_Equipo.json', orient='records')
print('JSON creado correctamente')