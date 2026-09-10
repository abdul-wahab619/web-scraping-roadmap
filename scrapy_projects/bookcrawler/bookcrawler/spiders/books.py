import scrapy
from bookcrawler.items import BookcrawlerItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        books = response.xpath(".//article[contains(@class, 'product_pod')]")
        print(f"Found {len(books)} books on the page.")

        for book in books:
            title = book.xpath(".//h3/a/@title").get()

            price = book.xpath(".//p[contains(@class, 'price_color')]/text()").get()

            rating_class = book.xpath(
                ".//p[contains(@class, 'star-rating')]/@class"
            ).get()

            rating = rating_class.split()[-1]

            relative_url = book.xpath(".//h3/a/@href").get()
            url = response.urljoin(relative_url)

            item = BookcrawlerItem(title=title, price=price, rating=rating, url=url)

            yield item

        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if next_page:
            next_page_url = response.urljoin(next_page)

            yield scrapy.Request(next_page_url, callback=self.parse)
