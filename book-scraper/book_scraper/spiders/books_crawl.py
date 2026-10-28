
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from book_scraper.loaders import BookLoader


class BooksCrawlSpider(CrawlSpider):
    name = "books_crawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    
# Match pagination links using CSS
# LinkExtractor(
#     restrict_css=("li.next a",),
# )


# Restrict links by URL pattern
# LinkExtractor(
#     allow=(r"page-\d+\.html$",),
#     restrict_css=("li.next a",),
# )

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//li[@class="next"]/a',),
            ),
            callback="parse_books",
            follow=True,
        ),
    )

    def parse_start_url(self, response):
        """Parse the initial page; CrawlSpider rules handle later pages."""
        yield from self.parse_books(response)

    def parse_books(self, response):
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
            loader.add_css(
                "availability",
                ".availability::text",
            )

            product_url = book.css(
                "h3 a::attr(href)"
            ).get()

            image_url = book.css(
                "div.image_container img::attr(src)"
            ).get()

            loader.add_value(
                "product_url",
                response.urljoin(product_url)
                if product_url else None,
            )

            loader.add_value(
                "image_url",
                response.urljoin(image_url)
                if image_url else None,
            )

            yield loader.load_item()
