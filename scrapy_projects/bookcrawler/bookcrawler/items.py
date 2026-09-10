# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class BookcrawlerItem:
    # define the fields for your item here like:
    title: str | None = None
    price: str | None = None
    rating: str | None = None
    url: str | None = None
    # name: str | None = None
    pass
