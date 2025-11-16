import scrapy

class ScrapyFEB(scrapy.Spider):
    name = "FEB_xpath"
    allowed_domains = ["www.primerafeb.com"]
    start_urls = ["https://www.primerafeb.com/estadisticas.aspx"]

    def parse(self, response):

        tabla_estadistica = response.xpath("(//table[contains(@class, 'tabla-estadistica')])[1]")
        filas = tabla_estadistica.xpath(".//tr")

        temporada_actual = response.xpath("//select[@id='_ctl0_temporadasDropDownList']/option[@selected]/text()").get()

        for fila in filas:
            nombre = fila.xpath(".//td[contains(@class, 'equipo')]/a/text()").get()
            puntos = fila.xpath(".//td[contains(@class, 'puntos')]/text()").get()
            asistencias = fila.xpath(".//td[contains(@class, 'asistencias')]/text()").get()
            valoracion = fila.xpath(".//td[contains(@class, 'valoracion')]/text()").get()
            triples = fila.xpath(".//td[contains(@class, 'tiros3')]/text()").get()
            mates = fila.xpath(".//td[contains(@class, 'mates')]/text()").get()

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
