from bookcrawler.items import BookcrawlerItem
from bookcrawler.pipelines import BookValidationPipeline
from bookcrawler.pipelines import DuplicateBookPipeline

# pipeline = BookValidationPipeline()

# item = BookcrawlerItem(
#     title="Test Book",
#     url="https://example.com/book",
#     upc="123456789",
#     price=20.0,
#     price_excl_tax=18.0,
#     price_incl_tax=20.0,
#     tax=2.0,
#     rating=5,
#     number_of_reviews=10,
# )

# result = pipeline.process_item(item)

# print(result)

pipeline = DuplicateBookPipeline()

item1 = BookcrawlerItem(
    title="Book One",
    url="https://example.com/book1",
    upc="123456789",
)

item2 = BookcrawlerItem(
    title="Book Two",
    url="https://example.com/book2",
    upc="123456789",
)

print("FIRST ITEM:")
print(pipeline.process_item(item1))

print("\nSECOND ITEM:")
print(pipeline.process_item(item2))
