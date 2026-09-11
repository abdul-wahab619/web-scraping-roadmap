import scrapy
from bookcrawler.items import BookcrawlerItem

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_int(value):
    if not value:
        return None

    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None


def parse_money(value):
    if not value:
        return None

    try:
        return float(value.replace("£", "").strip())
    except (ValueError, AttributeError):
        return None


class BooksSpider(scrapy.Spider):

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def log_missing_field(self, field_name, value, url):
        if value is None:
            self.logger.warning(
                "Missing field '%s' | URL: %s",
                field_name,
                url,
            )

    def closed(self, reason):
        self.logger.info(
            "Missing prices: %s",
            self.missing_price_count,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.missing_price_count = 0

    # async def start(self):
    #     yield scrapy.Request(
    #         "https://httpbin.org/get",
    #         callback=self.parse_test,
    #         errback=self.handle_error,
    #     )

    # def parse_test(self, response):
    #     print("STATUS:", response.status)

    # def handle_error(self, failure):
    #     print("REQUEST FAILED")
    #     print("EXCEPTION:", failure.type.__name__)
    #     print("VALUE:", failure.value)

    def parse(self, response):

        if response.status != 200:
            self.logger.warning(
                "Unexpected status %s: %s",
                response.status,
                response.url,
            )
            return

        books = response.xpath(".//article[contains(@class, 'product_pod')]")

        for book in books:
            detail_url = book.xpath(".//h3/a/@href").get()

            if detail_url:
                yield response.follow(detail_url, callback=self.parse_detail)

        # 4. Find next page
        next_page = response.xpath("//li[@class='next']/a/@href").get()

        # 5. Follow next page
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):

        if response.status != 200:
            self.logger.warning(
                "Unexpected detail status %s: %s",
                response.status,
                response.url,
            )
            return

        title = response.xpath(
            "//div[contains(@class, 'product_main')]/h1/text()"
        ).get()
        if title:
            title = title.strip()
        else:
            self.logger.warning(
                "Missing field 'title' | URL: %s",
                response.url,
            )
            title = "Unknown"

        price = response.xpath(
            "//div[contains(@class, 'product_main')]//p[contains(@class, 'price_color')]/text()"
        ).get()

        price = parse_money(price)
        if price is None:
            self.missing_price_count += 1
            self.log_missing_field("price", price, response.url)

        rating_class = response.xpath(
            "//div[contains(@class, 'product_main')]//p[contains(@class, 'star-rating')]/@class"
        ).get()

        rating_name = rating_class.split()[-1] if rating_class else None
        rating = rating_map.get(rating_name) if rating_name else None

        url = response.url

        # Detail-page fields will be extracted here
        upc = response.xpath("//th[text()='UPC']/following-sibling::td/text()").get()
        self.log_missing_field("upc", upc, response.url)

        product_type = response.xpath(
            "//th[text()='Product Type']/following-sibling::td/text()"
        ).get()

        price_excl_tax = response.xpath(
            "//th[text()='Price (excl. tax)']/following-sibling::td/text()"
        ).get()

        price_excl_tax = parse_money(price_excl_tax)

        price_incl_tax = response.xpath(
            "//th[text()='Price (incl. tax)']/following-sibling::td/text()"
        ).get()
        price_incl_tax = parse_money(price_incl_tax)

        tax = response.xpath("//th[text()='Tax']/following-sibling::td/text()").get()
        tax = parse_money(tax)

        availability = response.xpath(
            "//th[text()='Availability']/following-sibling::td/text()"
        ).get()

        availability = availability.strip() if availability else None

        number_of_reviews = response.xpath(
            "//th[text()='Number of reviews']/following-sibling::td/text()"
        ).get()
        number_of_reviews = parse_int(number_of_reviews)

        description = response.xpath(
            "//div[@id='product_description']/following-sibling::p[1]/text()"
        ).get()

        yield BookcrawlerItem(
            title=title,
            price=price,
            rating=rating,
            url=url,
            upc=upc,
            product_type=product_type,
            price_excl_tax=price_excl_tax,
            price_incl_tax=price_incl_tax,
            tax=tax,
            availability=availability,
            number_of_reviews=number_of_reviews,
            description=description,
        )
