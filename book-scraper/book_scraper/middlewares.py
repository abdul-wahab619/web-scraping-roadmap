# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging

from scrapy.exceptions import IgnoreRequest
from twisted.internet import reactor

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

    def __init__(self, stats, crawler):
        self.stats = stats
        self.crawler = crawler
        self.logger = logging.getLogger(self.__class__.__name__)
        self._shutdown_scheduled = False

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            stats=crawler.stats,
            crawler=crawler,
        )

    def process_request(self, request, spider):
        self.stats.inc_value("book_scraper/requests_seen")

        self.logger.debug(
            "Processing request: %s",
            request.url,
        )

        return None

    def process_response(self, request, response, spider):
        self.stats.inc_value("book_scraper/responses_received")

        status = response.status

        status_categories = {
            407: ("proxy_auth_required", "Proxy authentication required"),
            403: ("access_denied", "Access denied"),
            408: ("request_timeout", "Request timeout"),
            429: ("rate_limited", "Rate limited"),
            503: ("service_unavailable", "Service unavailable"),
        }

        if status in status_categories:
            stat_name, description = status_categories[status]

            self.stats.inc_value(f"book_scraper/http/{stat_name}")

            self.logger.warning(
                "%s: HTTP %s received for %s",
                description,
                status,
                request.url,
            )

        if status == 403 and not self._shutdown_scheduled:
            self._shutdown_scheduled = True

            self.logger.error("HTTP 403 received. Scheduling spider shutdown.")

            reactor.callLater(
                0,
                self._close_spider,
                spider,
            )

        challenge_type = self.detect_bot_challenge(response)

        if challenge_type:
            self.stats.inc_value(f"book_scraper/anti_bot/{challenge_type}")

            self.logger.error(
                "Bot challenge detected (%s): %s",
                challenge_type,
                response.url,
            )

            if not self._shutdown_scheduled:
                self._shutdown_scheduled = True

                reactor.callLater(
                    0,
                    self._close_spider,
                    spider,
                )

        return response

    def process_exception(self, request, exception, spider):
        self.stats.inc_value("book_scraper/download_exceptions")

        if isinstance(exception, IgnoreRequest):
            self.logger.debug(
                "Request ignored: %s",
                request.url,
            )
            return None

        exception_name = exception.__class__.__name__
        exception_message = str(exception).lower()

        proxy_error_categories = {
            "connection_refused": (
                "ConnectionRefusedError",
                "connection refused",
            ),
            "connection_timeout": (
                "TimeoutError",
                "timed out",
            ),
            "dns_failure": (
                "DNSLookupError",
                "name or service not known",
            ),
            "proxy_tunnel_failure": (
                "TunnelError",
                "tunnel",
            ),
        }

        matched_category = None

        for category, indicators in proxy_error_categories.items():
            if exception_name == indicators[0] or indicators[1] in exception_message:
                matched_category = category
                break

        if matched_category:
            self.stats.inc_value(f"book_scraper/proxy_failures/{matched_category}")

            self.logger.error(
                "Proxy failure (%s): %s",
                matched_category,
                exception,
            )

        else:
            self.stats.inc_value("book_scraper/download_exceptions/other")

            self.logger.error(
                "Download exception (%s): %s",
                exception_name,
                exception,
            )

        return None

    def detect_bot_challenge(self, response):
        body = response.text.lower()

        indicators = {
            "captcha": [
                "captcha",
                "g-recaptcha",
                "h-captcha",
            ],
            "cloudflare": [
                "cf-chl-",
                "challenge-platform",
                "just a moment...",
            ],
            "generic_challenge": [
                "verify you are human",
                "unusual traffic",
                "automated requests",
            ],
        }

        for challenge_type, keywords in indicators.items():
            if any(keyword in body for keyword in keywords):
                return challenge_type

        return None

    def _close_spider(self, spider):
        if self.crawler.engine is None:
            return

        self.crawler.engine.close_spider(
            spider,
            reason="access_denied",
        )
