import scrapy

class ScrapyFEB(scrapy.Spider):
    name = "FEB_css"
    allowed_domains = ["www.primerafeb.com"]
    start_urls = ["https://www.primerafeb.com/estadisticas.aspx"]

    def parse(self, response):
        
        tabla_estadistica = response.css("table.tabla-estadistica")[0]
        filas = tabla_estadistica.css("tr")

        temporada_actual = response.css("select#_ctl0_temporadasDropDownList option[selected]::text").get()

        for fila in filas:
            nombre = fila.css("td.equipo a::text").get()
            puntos = fila.css("td.puntos::text").get()
            asistencias = fila.css("td.asistencias::text").get()
            valoracion = fila.css("td.valoracion::text").get()
            triples = fila.css("td.tiros3::text").get()
            mates = fila.css("td.mates::text").get()
            
            if nombre:
                items = {
                    "Temporada": temporada_actual.strip() if temporada_actual else "None",
                    "Nombre": nombre.strip(),
                    "Puntos": puntos.strip(),
                    "Asistencia": asistencias.strip(),
                    "Valoracion": valoracion.strip(),
                    "Triples": triples.strip(),
                    "Mates": mates.strip() if mates else None,
                }
                yield items

