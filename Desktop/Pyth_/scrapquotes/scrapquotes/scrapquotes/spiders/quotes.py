import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        # Парсинг цитат и авторов
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        # Переход на следующую страницу
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

