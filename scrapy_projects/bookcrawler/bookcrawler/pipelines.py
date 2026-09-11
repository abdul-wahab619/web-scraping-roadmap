# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


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

        required_fields = ["title", "url", "upc"]

        for field in required_fields:
            value = adapter.get(field)

            if not value:
                raise DropItem(f"Missing required field: {field}")

        # Validate price
        price = adapter.get("price")

        if price is not None and price < 0:
            raise DropItem(f"Invalid price: {price}")

        price_excl_tax = adapter.get("price_excl_tax")

        if price_excl_tax is not None and price_excl_tax < 0:
            raise DropItem(f"Invalid price_excl_tax: {price_excl_tax}")

        price_incl_tax = adapter.get("price_incl_tax")

        if price_incl_tax is not None and price_incl_tax < 0:
            raise DropItem(f"Invalid price_incl_tax: {price_incl_tax}")

        if (
            price_excl_tax is not None
            and price_incl_tax is not None
            and price_incl_tax < price_excl_tax
        ):
            raise DropItem(
                f"Invalid price relationship: "
                f"incl={price_incl_tax}, excl={price_excl_tax}"
            )

        tax = adapter.get("tax")

        if tax is not None and tax < 0:
            raise DropItem(f"Invalid tax: {tax}")

        # Validate rating
        rating = adapter.get("rating")

        if rating is not None and not 1 <= rating <= 5:
            raise DropItem(f"Invalid rating: {rating}")

        # Validate number of reviews
        number_of_reviews = adapter.get("number_of_reviews")

        if number_of_reviews is not None and number_of_reviews < 0:
            raise DropItem(f"Invalid reviews: {number_of_reviews}")

        return item


class DuplicateBookPipeline:
    def __init__(self):
        self.seen_upcs = set()

    def process_item(self, item):

        adapter = ItemAdapter(item)

        # upc
        upc = adapter.get("upc")

        if upc:
            if upc in self.seen_upcs:
                raise DropItem(f"Duplicate book: {upc}")

            self.seen_upcs.add(upc)

        return item
