import logging

from scrapy import signals


logger = logging.getLogger(__name__)


class CrawlMonitoringExtension:

    def __init__(self):
        self.items_scraped = 0
        self.items_dropped = 0

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls()

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
            extension.spider_closed,
            signal=signals.spider_closed,
        )

        return extension

    def spider_opened(self, spider):
        logger.info(
            "MONITOR: Spider started | name=%s",
            spider.name,
        )

    def item_scraped(self, item, spider):
        self.items_scraped += 1

    def item_dropped(self, item, exception, spider):
        self.items_dropped += 1

        logger.warning(
            "MONITOR: Item dropped | spider=%s | reason=%s",
            spider.name,
            exception,
        )

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats

        requests = stats.get_value(
            "downloader/request_count",
            0,
        )

        retries = stats.get_value(
            "retry/count",
            0,
        )

        elapsed = stats.get_value(
            "elapsed_time_seconds",
            0,
        )

        logger.info("========== CRAWL REPORT ==========")
        logger.info("Spider: %s", spider.name)
        logger.info("Items scraped: %s", self.items_scraped)
        logger.info("Items dropped: %s", self.items_dropped)
        logger.info("Requests: %s", requests)
        logger.info("Retries: %s", retries)
        logger.info("Elapsed time: %.2fs", elapsed)
        logger.info("Finish reason: %s", reason)
        logger.info("==================================")