
from urllib.parse import urljoin

from web_poet.pages import WebPage

from book_scraper.loaders import (
    clean_text,
    parse_availability,
    parse_price,
    parse_rating,
)


class BooksListingPage(WebPage):
    """Extract book records from a Books to Scrape listing page."""

    def books(self):
        for book in self.css("article.product_pod"):
            title = book.css("h3 a::attr(title)").get()
            price = book.css(".price_color::text").get()
            rating_class = book.css(
                "p.star-rating::attr(class)"
            ).get()
            availability = book.css(
                ".availability::text"
            ).getall()

            product_href = book.css(
                "h3 a::attr(href)"
            ).get()
            image_href = book.css(
                "div.image_container img::attr(src)"
            ).get()

            yield {
                "title": clean_text(title) if title else None,
                "price": parse_price(price) if price else None,
                "rating": (
                    parse_rating(rating_class)
                    if rating_class
                    else None
                ),
                "availability": parse_availability(availability),
                "product_url": (
                    urljoin(self.url, product_href)
                    if product_href
                    else None
                ),
                "image_url": (
                    urljoin(self.url, image_href)
                    if image_href
                    else None
                ),
            }
