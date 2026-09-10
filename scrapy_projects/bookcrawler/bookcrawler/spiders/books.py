import scrapy
from bookcrawler.items import BookcrawlerItem

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        books = response.xpath(".//article[contains(@class, 'product_pod')]")
        print(f"Found {len(books)} books on the page.")

        for book in books:
            title = book.xpath(".//h3/a/@title").get()

            price_text = book.xpath(
                ".//p[contains(@class, 'price_color')]/text()"
            ).get()

            price = price_text.strip() if price_text else None

            rating_class = book.xpath(
                ".//p[contains(@class, 'star-rating')]/@class"
            ).get()

            rating_name = rating_class.split()[-1] if rating_class else None

            rating = rating_map.get(rating_name) if rating_name else None

            relative_url = book.xpath(".//h3/a/@href").get()
            url = response.urljoin(relative_url)

            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                meta={
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": url,
                },
            )

        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if next_page:
            next_page_url = response.urljoin(next_page)

            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        title = response.meta["title"]
        price = response.meta["price"]
        rating = response.meta["rating"]
        url = response.meta["url"]

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
