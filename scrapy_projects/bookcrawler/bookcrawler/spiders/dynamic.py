import scrapy
from bookcrawler.items import QuoteItem


class DynamicSpider(scrapy.Spider):

    name = "dynamic"
    allowed_domains = ["quotes.toscrape.com"]

    async def start(self):
        yield scrapy.Request(
            "https://quotes.toscrape.com/js/",
            meta={
                "playwright": True,
            },
            callback=self.parse,
        )

    def parse(self, response):

        quotes = response.css("div.quote")

        self.logger.info(
            "Quotes found: %s",
            len(quotes),
        )

        for quote in quotes:
            yield QuoteItem(
                text=quote.css("span.text::text").get(),
                author=quote.css("small.author::text").get(),
            )
