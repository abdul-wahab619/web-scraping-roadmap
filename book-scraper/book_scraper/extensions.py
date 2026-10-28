
import time

from scrapy import signals


class CrawlStatsExtension:
    """Track crawl duration, items, drops, and spider errors."""

    def __init__(self, stats):
        self.stats = stats
        self.started_at = None

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls(crawler.stats)

        crawler.signals.connect(
            extension.spider_opened,
            signal=signals.spider_opened,
        )
        crawler.signals.connect(
            extension.item_scraped,
            signal=signals.item_scraped,
        )
        crawler.signals.connect(
            extension.item_dropped,
            signal=signals.item_dropped,
        )
        crawler.signals.connect(
            extension.spider_error,
            signal=signals.spider_error,
        )
        crawler.signals.connect(
            extension.spider_closed,
            signal=signals.spider_closed,
        )

        return extension

    def spider_opened(self, spider):
        self.started_at = time.monotonic()

        self.stats.set_value(
            "book_scraper/items_scraped",
            0,
        )
        self.stats.set_value(
            "book_scraper/items_dropped",
            0,
        )
        self.stats.set_value(
            "book_scraper/spider_errors",
            0,
        )

        spider.logger.info(
            "CrawlStatsExtension started."
        )

    def item_scraped(self, item, response, spider):
        self.stats.inc_value(
            "book_scraper/items_scraped"
        )

    def item_dropped(self, item, response, exception, spider):
        self.stats.inc_value(
            "book_scraper/items_dropped"
        )

        spider.logger.warning(
            "Item dropped: %s",
            exception,
        )

    def spider_error(self, failure, response, spider):
        self.stats.inc_value(
            "book_scraper/spider_errors"
        )

        spider.logger.error(
            "Spider error on %s: %s",
            response.url if response else "unknown URL",
            failure.getErrorMessage(),
        )

    def spider_closed(self, spider, reason):
        duration = (
            time.monotonic() - self.started_at
            if self.started_at is not None
            else 0
        )

        self.stats.set_value(
            "book_scraper/duration_seconds",
            round(duration, 2),
        )

        spider.logger.info(
            "Crawl summary | reason=%s | duration=%.2fs "
            "| scraped=%s | dropped=%s | spider_errors=%s",
            reason,
            duration,
            self.stats.get_value(
                "book_scraper/items_scraped", 0
            ),
            self.stats.get_value(
                "book_scraper/items_dropped", 0
            ),
            self.stats.get_value(
                "book_scraper/spider_errors", 0
            ),
        )
