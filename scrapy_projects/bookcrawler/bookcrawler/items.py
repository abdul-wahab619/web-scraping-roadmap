# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class QuoteItem:
    text: str | None = None
    author: str | None = None


@dataclass
class BookcrawlerItem:
    title: str | None = None
    price: float | None = None
    rating: int | None = None
    url: str | None = None

    upc: str | None = None
    product_type: str | None = None
    price_excl_tax: float | None = None
    price_incl_tax: float | None = None
    tax: float | None = None
    availability: str | None = None
    number_of_reviews: int | None = None
    description: str | None = None
