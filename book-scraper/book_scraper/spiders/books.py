import scrapy

from book_scraper.loaders import BookLoader, parse_availability


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("article.product_pod")

        self.logger.info(
            "Found %d books on %s",
            len(books),
            response.url,
        )

        for book in books:
            loader = BookLoader(
                selector=book,
                response=response,
            )

            loader.add_css("title", "h3 a::attr(title)")
            loader.add_css("price", ".price_color::text")
            loader.add_css(
                "rating",
                "p.star-rating::attr(class)",
            )
            product_url = book.css("h3 a::attr(href)").get()

            image_url = book.css("div.image_container img::attr(src)").get()

            loader.add_value(
                "product_url",
                response.urljoin(product_url) if product_url else None,
            )

            loader.add_value(
                "image_url",
                response.urljoin(image_url) if image_url else None,
            )

            item = loader.load_item()

            if product_url:
                yield response.follow(
                    product_url,
                    callback=self.parse_product,
                    meta={"item": item},
                )
            else:
                item["availability"] = parse_availability([])
                yield item

        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
            )

    def parse_product(self, response):
        item = response.meta["item"]
        item["availability"] = parse_availability(
            response.css(".product_main .availability::text").getall()
        )
        yield item
