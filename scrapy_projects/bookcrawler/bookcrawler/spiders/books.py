import scrapy
from bookcrawler.items import BookcrawlerItem

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BooksSpider(scrapy.Spider):

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

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

        title = response.xpath(
            "//div[contains(@class, 'product_main')]/h1/text()"
        ).get()

        price = response.xpath(
            "//div[contains(@class, 'product_main')]//p[contains(@class, 'price_color')]/text()"
        ).get()

        rating_class = response.xpath(
            "//div[contains(@class, 'product_main')]//p[contains(@class, 'star-rating')]/@class"
        ).get()

        rating_name = rating_class.split()[-1] if rating_class else None
        rating = rating_map.get(rating_name) if rating_name else None

        url = response.url

        # Detail-page fields will be extracted here
        upc = response.xpath("//th[text()='UPC']/following-sibling::td/text()").get()

        product_type = response.xpath(
            "//th[text()='Product Type']/following-sibling::td/text()"
        ).get()

        price_excl_tax = response.xpath(
            "//th[text()='Price (excl. tax)']/following-sibling::td/text()"
        ).get()

        price_excl_tax = price_excl_tax.strip() if price_excl_tax else None

        price_incl_tax = response.xpath(
            "//th[text()='Price (incl. tax)']/following-sibling::td/text()"
        ).get()
        price_incl_tax = price_incl_tax.strip() if price_incl_tax else None

        tax = response.xpath("//th[text()='Tax']/following-sibling::td/text()").get()
        tax = tax.strip() if tax else None

        availability = response.xpath(
            "//th[text()='Availability']/following-sibling::td/text()"
        ).get()

        availability = availability.strip() if availability else None

        number_of_reviews = response.xpath(
            "//th[text()='Number of reviews']/following-sibling::td/text()"
        ).get()
        number_of_reviews = number_of_reviews.strip() if number_of_reviews else None

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
