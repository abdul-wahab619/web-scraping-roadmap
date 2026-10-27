import re
from decimal import Decimal, InvalidOperation

from itemloaders import ItemLoader
from itemloaders.processors import (
    Compose,
    MapCompose,
    TakeFirst,
)

from book_scraper.items import BookItem


def clean_text(value):
    return " ".join(value.split())


def parse_price(value):
    value = clean_text(value).replace("£", "").strip()

    try:
        return float(Decimal(value))
    except (InvalidOperation, ValueError):
        return None


def parse_rating(value):
    # HTML example: "star-rating Three"
    parts = clean_text(value).split()

    if len(parts) < 2:
        return None

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    return ratings.get(parts[-1])


def parse_availability(values):
    text = " ".join(values)
    text = clean_text(text)

    match = re.search(r"\d+", text)
    stock_count = int(match.group()) if match else 0

    return {
        "in_stock": "in stock" in text.lower(),
        "stock_count": stock_count,
    }


class BookLoader(ItemLoader):
    default_item_class = BookItem

    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    title_in = MapCompose(clean_text)
    title_out = TakeFirst()

    price_in = MapCompose(clean_text, parse_price)
    price_out = TakeFirst()

    rating_in = MapCompose(clean_text, parse_rating)
    rating_out = TakeFirst()

    availability_in = MapCompose(clean_text)
    availability_out = Compose(parse_availability)

    product_url_in = MapCompose(clean_text)
    product_url_out = TakeFirst()

    image_url_in = MapCompose(clean_text)
    image_url_out = TakeFirst()
