import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    allowed_domains = ["books.toscrape.com"]

    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        self.logger.info(
            "Fetched %s | HTTP status: %s",
            response.url,
            response.status,
        )

        books = response.css("article.product_pod")

        self.logger.info(
            "Found %s books on this page",
            len(books),
        )

        for book in books:
            title = book.css("h3 a::attr(title)").get()
            price = book.css(".price_color::text").get()
            rating_class = book.css("p.star-rating::attr(class)").get()
            availability = book.css(".availability::text").getall()

            yield {
                "title": title,
                "price": price,
                "rating_class": rating_class,
                "availability": " ".join(
                    value.strip() for value in availability if value.strip()
                ),
            }

        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
            )
