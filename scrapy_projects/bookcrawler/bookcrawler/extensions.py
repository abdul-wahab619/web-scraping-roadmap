import logging

from scrapy import signals

logger = logging.getLogger(__name__)


class CrawlMonitoringExtension:

    def __init__(self):
        self.items_scraped = 0
        self.items_dropped = 0
        self.drop_reasons = {}

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

        reason = str(exception)

        self.drop_reasons[reason] = self.drop_reasons.get(reason, 0) + 1

        logger.warning(
            "MONITOR: Item dropped | spider=%s | reason=%s",
            spider.name,
            reason,
        )

    def spider_closed(self, spider, reason):

        logger.info("========== DATA QUALITY REPORT ==========")

        logger.info(
            "Items scraped: %s",
            self.items_scraped,
        )

        logger.info(
            "Items dropped: %s",
            self.items_dropped,
        )

        total = self.items_scraped + self.items_dropped

        if total:
            quality_score = (self.items_scraped / total) * 100
        else:
            quality_score = 0

        logger.info(
            "Data quality: %.2f%%",
            quality_score,
        )

        if self.drop_reasons:
            logger.info("Drop reasons:")

            for drop_reason, count in self.drop_reasons.items():
                logger.info(
                    "  %s: %s",
                    drop_reason,
                    count,
                )

        if quality_score < 95:
            logger.error(
                "DATA QUALITY ALERT: %.2f%%",
                quality_score,
            )
        else:
            logger.info(
                "DATA QUALITY: %.2f%%",
                quality_score,
            )

        logger.info("========================================")
