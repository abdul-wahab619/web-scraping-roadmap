import scrapy


class CrawlZeroItemsTestSpider(scrapy.Spider):
    name = "crawl_zero_items_test"
    source_name = "remotive"

    async def start(self):
        yield scrapy.Request(
            url="https://example.com",
            callback=self.parse,
        )

    def parse(self, response):
        self.logger.info(
            "Zero-item test response received: %s",
            response.status,
        )

        # Intentionally yield no items.
        return
