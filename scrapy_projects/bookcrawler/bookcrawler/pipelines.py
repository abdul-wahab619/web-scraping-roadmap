# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
