
from spidermon import Monitor, MonitorSuite, monitors


@monitors.name("Book Crawl Health")
class BookCrawlHealthMonitor(Monitor):

    @monitors.name("Minimum number of books")
    def test_minimum_number_of_books(self):
        item_count = getattr(
            self.data.stats,
            "item_scraped_count",
            0,
        )

        minimum_threshold = 100

        self.assertGreaterEqual(
            item_count,
            minimum_threshold,
            msg=(
                f"Expected at least {minimum_threshold} books, "
                f"but scraped {item_count}."
            ),
        )

    @monitors.name("At least one book scraped")
    def test_at_least_one_book_scraped(self):
        item_count = getattr(
            self.data.stats,
            "item_scraped_count",
            0,
        )

        self.assertGreater(
            item_count,
            0,
            msg="The crawl finished without scraping any books.",
        )


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        BookCrawlHealthMonitor,
    ]
