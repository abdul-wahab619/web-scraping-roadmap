
import scrapy

from book_scraper.pages import BooksListingPage


class BooksPoetSpider(scrapy.Spider):
    name = "books_poet"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response, page: BooksListingPage):
        self.logger.info("Processing listing: %s", response.url)

        for item in page.books():
            yield item

        next_page = response.css(
            "li.next a::attr(href)"
        ).get()

        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
            )
