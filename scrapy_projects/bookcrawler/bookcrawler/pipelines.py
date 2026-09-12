from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from urllib.parse import urlparse


def is_valid_url(value):
    if not value:
        return False

    parsed = urlparse(value)

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class BookcrawlerPipeline:
    def process_item(self, item):
        adapter = ItemAdapter(item)

        # Clean string fields
        for field in [
            "title",
            "product_type",
            "availability",
            "description",
        ]:
            value = adapter.get(field)

            if isinstance(value, str):
                adapter[field] = value.strip()

        # Convert price fields to float
        for field in [
            "price",
            "price_excl_tax",
            "price_incl_tax",
            "tax",
        ]:
            value = adapter.get(field)

            if isinstance(value, str):
                adapter[field] = float(value.replace("£", "").strip())

        # Convert reviews to int
        value = adapter.get("number_of_reviews")

        if isinstance(value, str):
            adapter["number_of_reviews"] = int(value.strip())

        return item


class BookValidationPipeline:
    def process_item(self, item):
        adapter = ItemAdapter(item)

        # --------------------------------
        # Required fields
        # --------------------------------

        required_fields = ["title", "url", "upc"]

        for field in required_fields:
            value = adapter.get(field)

            if not value:
                raise DropItem(f"Missing required field: {field}")

        # --------------------------------
        # Validate title
        # --------------------------------

        title = adapter.get("title")

        if not isinstance(title, str) or not title.strip():
            raise DropItem("Invalid title")

        # --------------------------------
        # Validate URL
        # --------------------------------

        url = adapter.get("url")

        if not is_valid_url(url):
            raise DropItem(f"Invalid URL: {url}")

        # --------------------------------
        # Validate UPC
        # --------------------------------

        upc = adapter.get("upc")

        if not isinstance(upc, str) or not upc.strip():
            raise DropItem("Invalid UPC")

        # --------------------------------
        # Validate numeric types
        # --------------------------------

        numeric_fields = [
            "price",
            "price_excl_tax",
            "price_incl_tax",
            "tax",
            "rating",
            "number_of_reviews",
        ]

        for field in numeric_fields:
            value = adapter.get(field)

            if value is not None and not isinstance(value, (int, float)):
                raise DropItem(f"Invalid {field} type: {type(value).__name__}")

        # --------------------------------
        # Validate price
        # --------------------------------

        price = adapter.get("price")

        if price is not None and price < 0:
            raise DropItem(f"Invalid price: {price}")

        # --------------------------------
        # Validate price excluding tax
        # --------------------------------

        price_excl_tax = adapter.get("price_excl_tax")

        if price_excl_tax is not None and price_excl_tax < 0:
            raise DropItem(f"Invalid price_excl_tax: {price_excl_tax}")

        # --------------------------------
        # Validate price including tax
        # --------------------------------

        price_incl_tax = adapter.get("price_incl_tax")

        if price_incl_tax is not None and price_incl_tax < 0:
            raise DropItem(f"Invalid price_incl_tax: {price_incl_tax}")

        # --------------------------------
        # Validate price relationship
        # --------------------------------

        if (
            price_excl_tax is not None
            and price_incl_tax is not None
            and price_incl_tax < price_excl_tax
        ):
            raise DropItem(
                f"Invalid price relationship: "
                f"incl={price_incl_tax}, "
                f"excl={price_excl_tax}"
            )

        # --------------------------------
        # Validate tax
        # --------------------------------

        tax = adapter.get("tax")

        if tax is not None and tax < 0:
            raise DropItem(f"Invalid tax: {tax}")

        # --------------------------------
        # Validate rating
        # --------------------------------

        rating = adapter.get("rating")

        if rating is not None and not 1 <= rating <= 5:
            raise DropItem(f"Invalid rating: {rating}")

        # --------------------------------
        # Validate number of reviews
        # --------------------------------

        number_of_reviews = adapter.get("number_of_reviews")

        if number_of_reviews is not None and number_of_reviews < 0:
            raise DropItem(f"Invalid reviews: {number_of_reviews}")

        return item


class DuplicateBookPipeline:

    def __init__(self):
        self.seen_upcs = set()

    def process_item(self, item):

        adapter = ItemAdapter(item)

        upc = adapter.get("upc")

        if upc:
            if upc in self.seen_upcs:
                raise DropItem(f"Duplicate book: {upc}")

            self.seen_upcs.add(upc)

        return item


class DataQualityPipeline:

    def __init__(self):
        self.dropped_items = 0
        self.drop_reasons = {}

    def process_item(self, item):
        return item

    def close_spider(self, spider):
        spider.logger.info("========== DATA QUALITY REPORT ==========")
        spider.logger.info(
            "Items dropped: %s",
            self.dropped_items,
        )

        for reason, count in self.drop_reasons.items():
            spider.logger.info(
                "%s: %s",
                reason,
                count,
            )

        spider.logger.info("========================================")
