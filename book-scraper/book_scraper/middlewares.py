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
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        middleware.crawler = crawler
        middleware.stats = crawler.stats
        return middleware

    def process_request(self, request):
        self.stats.inc_value("book_scraper/requests_seen")

        spider = self.crawler.spider
        if spider:
            spider.logger.debug("Outgoing request: %s", request.url)

        return None

    def process_response(self, request, response):
        self.stats.inc_value("book_scraper/responses_received")

        spider = self.crawler.spider
        if spider:
            if response.status == 407 and request.meta.get("proxy"):
                self.stats.inc_value("book_scraper/proxy_auth_failures")
                spider.logger.error(
                    "Proxy authentication failed (HTTP 407) for %s",
                    request.url,
                )

            spider.logger.debug(
                "Received HTTP %s: %s",
                response.status,
                response.url,
            )

        return response

    def process_exception(self, request, exception):
        self.stats.inc_value("book_scraper/download_exceptions")

        spider = self.crawler.spider
        if not spider:
            return None

        # Only classify failures for requests using a proxy.
        if request.meta.get("proxy"):
            exception_name = type(exception).__name__

            if "refused" in exception_name.lower():
                category = "connection_refused"
            elif "timeout" in exception_name.lower():
                category = "timeout"
            elif "tunnel" in exception_name.lower():
                category = "tunnel_error"
            elif "dns" in exception_name.lower():
                category = "dns_failure"
            else:
                category = "other"

            self.stats.inc_value(f"book_scraper/proxy_failures/{category}")

            spider.logger.warning(
                "Proxy failure [%s] for %s: %s",
                category,
                request.url,
                exception,
            )
        else:
            spider.logger.warning(
                "Download exception for %s: %s",
                request.url,
                exception,
            )

        # Let the retry middleware handle the exception.
        return None
