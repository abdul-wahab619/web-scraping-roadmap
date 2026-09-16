import scrapy


class CrawlFailureTestSpider(scrapy.Spider):
    name = "crawl_failure_test"
    source_name = "remotive"

    async def start(self):
        yield scrapy.Request(
            url="https://httpbin.org/status/500",
            callback=self.parse,
        )

    def parse(self, response):
        yield {}
