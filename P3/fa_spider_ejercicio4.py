import scrapy

domain = "proxy-cache-func-jldiaz-e9b7ddh6graybmfr.italynorth-01.azurewebsites.net"
proxy_url = f"https://{domain}/api/proxy"
path_url = "/es/ranking.php?rn=ranking_fa_movies"

class FaSpiderSpider(scrapy.Spider):
    name = "fa_spider"
    allowed_domains = [domain]
    start_urls = [f"{proxy_url}{path_url}"]

    def parse(self, response):
        # Usando selectores css
        for pelicula in response.css("div.movie-card"):
            titulo = pelicula.css("div.mc-title a::text").get()

            año = pelicula.css("span.mc-year::text").get()

            directores = pelicula.css("div.mc-director a::text").getall()

            print(f"{titulo} ({año}) - Director: {directores}")

        print("-" * 80)

        # Usando xpath
        for pelicula in response.xpath('//div[contains(@class, "movie-card")]'):
            titulo = pelicula.xpath('.//div[contains(@class, "mc-title")]/a/text()').get()

            año = pelicula.xpath('.//span[contains(@class, "mc-year")]/text()').get()

            directores = pelicula.xpath('.//div[contains(@class, "mc-director")]/a/text()').getall()

            print(f"{titulo} ({año}) - Director: {directores}")
