# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookScraperSpiderMiddleware:
    """Observe responses and items passing through the spider."""

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        middleware.crawler = crawler

        crawler.signals.connect(
            middleware.spider_opened,
            signal=signals.spider_opened,
        )
        return middleware

    def process_spider_input(self, response):
        spider = self.crawler.spider
        spider.logger.debug("Spider input: %s", response.url)
        return None

    def process_spider_output(self, response, result):
        for output in result:
            yield output

    async def process_spider_output_async(self, response, result):
        async for output in result:
            yield output

    def process_spider_exception(self, response, exception):
        spider = self.crawler.spider
        spider.logger.error(
            "Spider callback failed for %s: %s",
            response.url,
            exception,
        )
        return None

    async def process_start(self, start):
        async for item in start:
            yield item

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s", spider.name)


class BookScraperDownloaderMiddleware:
    """Log requests and responses for the book scraper."""

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        middleware.stats = crawler.stats
        return middleware

    def process_request(self, request, spider):
        self.stats.inc_value("book_scraper/requests_seen")

        spider.logger.debug(
            "Outgoing request: %s",
            request.url,
        )

        # None means continue through the downloader chain.
        return None

    def process_response(self, request, response, spider):
        self.stats.inc_value("book_scraper/responses_received")

        spider.logger.debug(
            "Received HTTP %s: %s",
            response.status,
            response.url,
        )

        return response

    def process_exception(self, request, exception, spider):
        self.stats.inc_value("book_scraper/download_exceptions")

        spider.logger.warning(
            "Download exception for %s: %s",
            request.url,
            exception,
        )

        # None allows other middleware to handle the exception.
        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
