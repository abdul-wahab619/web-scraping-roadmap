from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from urllib.parse import urlparse
from bookcrawler.items import BookcrawlerItem, QuoteItem, JobItem
from datetime import datetime, timezone
from scrapy import signals
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLPipeline:

    def __init__(self):
        self.crawl_run_id = None
        self.crawl_started_at = None
        self.items_found = 0
        self.source = None
        self.crawler = None
        self.connection = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()

        pipeline.crawler = crawler

        crawler.signals.connect(
            pipeline.spider_closed,
            signal=signals.spider_closed,
        )

        return pipeline

    def open_spider(self):
        spider = self.crawler.spider
        self.connection = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

        self.cursor = self.connection.cursor()

        self.source = getattr(spider, "source_name", spider.name)
        self.crawl_started_at = datetime.now(timezone.utc)

        print("PostgreSQL connection established")

        self.cursor.execute(
            """
            INSERT INTO crawl_runs (
                source,
                started_at,
                status,
                items_found
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                self.source,
                self.crawl_started_at,
                "running",
                0,
            ),
        )

        self.crawl_run_id = self.cursor.fetchone()[0]

        self.connection.commit()

        print(f"Started crawl run " f"id={self.crawl_run_id}, " f"source={self.source}")

    def process_item(self, item):
        self.items_found += 1
        # --------------------------------
        # Books
        # --------------------------------

        if isinstance(item, BookcrawlerItem):

            self.cursor.execute(
                """
                INSERT INTO books (
                    title,
                    price,
                    rating,
                    url,
                    upc,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    availability,
                    number_of_reviews,
                    description
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (upc)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    price = EXCLUDED.price,
                    rating = EXCLUDED.rating,
                    url = EXCLUDED.url,
                    product_type = EXCLUDED.product_type,
                    price_excl_tax = EXCLUDED.price_excl_tax,
                    price_incl_tax = EXCLUDED.price_incl_tax,
                    tax = EXCLUDED.tax,
                    availability = EXCLUDED.availability,
                    number_of_reviews = EXCLUDED.number_of_reviews,
                    description = EXCLUDED.description
                """,
                (
                    item.title,
                    item.price,
                    item.rating,
                    item.url,
                    item.upc,
                    item.product_type,
                    item.price_excl_tax,
                    item.price_incl_tax,
                    item.tax,
                    item.availability,
                    item.number_of_reviews,
                    item.description,
                ),
            )

            self.connection.commit()

            return item

        # --------------------------------
        # Jobs
        # --------------------------------
        if isinstance(item, JobItem):
            try:
                self.cursor.execute(
                    """
                        INSERT INTO jobs (
                            title,
                            company,
                            location,
                            job_type,
                            remote,
                            salary,
                            description,
                            url,
                            source,
                            external_id,
                            posted_at,
                            scraped_at,
                            last_seen_at
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s,
                            %s
                        )
                        ON CONFLICT (source, external_id)
                        DO UPDATE SET
                            title = EXCLUDED.title,
                            company = EXCLUDED.company,
                            location = EXCLUDED.location,
                            job_type = EXCLUDED.job_type,
                            remote = EXCLUDED.remote,
                            salary = EXCLUDED.salary,
                            description = EXCLUDED.description,
                            url = EXCLUDED.url,
                            posted_at = EXCLUDED.posted_at,
                            scraped_at = EXCLUDED.scraped_at,
                            last_seen_at = EXCLUDED.last_seen_at
                        """,
                    (
                        item.title,
                        item.company,
                        item.location,
                        item.job_type,
                        item.remote,
                        item.salary,
                        item.description,
                        item.url,
                        item.source,
                        item.external_id,
                        item.posted_at,
                        item.scraped_at,
                        item.last_seen_at,
                    ),
                )

                self.connection.commit()

            except Exception as e:
                self.connection.rollback()

                print("========== JOB DATABASE ERROR ==========")
                print(f"Error: {e}")
                print(f"Title: {item.title}")
                print(f"External ID: {item.external_id}")
                print(f"URL: {item.url}")
                print("========================================")

                raise

            return item
        return item

    # def close_spider(self):
    #     if self.cursor and self.crawl_run_id:

    #         self.cursor.execute(
    #             """
    #         UPDATE crawl_runs
    #         SET
    #             finished_at = %s,
    #             status = %s,
    #             items_found = %s
    #         WHERE id = %s
    #         """,
    #             (
    #                 datetime.now(timezone.utc),
    #                 "finished",
    #                 self.items_found,
    #                 self.crawl_run_id,
    #             ),
    #         )

    #     self.cursor.execute(
    #         """
    #         UPDATE jobs
    #         SET status = CASE
    #             WHEN last_seen_at < NOW() - INTERVAL '1 day'
    #                 THEN 'stale'
    #             ELSE 'active'
    #         END
    #         WHERE source = %s
    #         """,
    #         (self.source,),
    #     )

    #     self.connection.commit()

    #     print(
    #         f"Completed crawl run "
    #         f"id={self.crawl_run_id}, "
    #         f"items_found={self.items_found}"
    #     )

    #     self.cursor.close()

    #     if self.connection:
    #         self.connection.close()

    def spider_closed(self, spider, reason):
        if not self.cursor or not self.crawl_run_id:
            return

        exception_count = self.crawler.stats.get_value(
            "spider_exceptions/count",
            0,
        )

        http_error_count = self.crawler.stats.get_value(
            "httperror/response_ignored_count",
            0,
        )

        retry_max_reached = self.crawler.stats.get_value(
            "retry/max_reached",
            0,
        )

        if exception_count > 0:
            status = "failed"
            error_message = f"Spider encountered {exception_count} exception(s)"

        elif http_error_count > 0:
            status = "failed"
            error_message = f"HTTP error responses ignored: {http_error_count}"

        elif retry_max_reached > 0:
            status = "failed"
            error_message = f"Retry limit reached for {retry_max_reached} request(s)"

        else:
            status = "finished"
            error_message = None

        self.cursor.execute(
            """
            UPDATE crawl_runs
            SET
                finished_at = %s,
                status = %s,
                items_found = %s,
                error_message = %s
            WHERE id = %s
            """,
            (
                datetime.now(timezone.utc),
                status,
                self.items_found,
                error_message,
                self.crawl_run_id,
            ),
        )

        if status == "finished":
            self.cursor.execute(
                """
                UPDATE jobs
                SET status = CASE
                    WHEN last_seen_at < NOW() - INTERVAL '1 day'
                        THEN 'stale'
                    ELSE 'active'
                END
                WHERE source = %s
                """,
                (self.source,),
            )

        self.connection.commit()

        print(
            f"Completed crawl run "
            f"id={self.crawl_run_id}, "
            f"status={status}, "
            f"items_found={self.items_found}"
        )

        if error_message:
            print(f"Crawl error: {error_message}")

        self.cursor.close()
        self.connection.close()

        print("PostgreSQL connection closed")


def is_valid_url(value):
    if not value:
        return False

    parsed = urlparse(value)

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class BookcrawlerPipeline:
    def process_item(self, item):
        if not isinstance(item, BookcrawlerItem):
            return item
        adapter = ItemAdapter(item)

        # Clean string fields
        for field in [
            "title",
            "product_type",
            "availability",
            "description",
        ]:
            value = adapter.get(field)

            if isinstance(value, str):
                adapter[field] = value.strip()

        # Convert price fields to float
        for field in [
            "price",
            "price_excl_tax",
            "price_incl_tax",
            "tax",
        ]:
            value = adapter.get(field)

            if isinstance(value, str):
                adapter[field] = float(value.replace("£", "").strip())

        # Convert reviews to int
        value = adapter.get("number_of_reviews")

        if isinstance(value, str):
            adapter["number_of_reviews"] = int(value.strip())

        return item


class BookValidationPipeline:

    def process_item(self, item):

        if not isinstance(item, BookcrawlerItem):
            return item

        adapter = ItemAdapter(item)

        # --------------------------------
        # Required fields
        # --------------------------------

        required_fields = ["title", "url", "upc"]

        for field in required_fields:
            value = adapter.get(field)

            if not value:
                raise DropItem(f"Missing required field: {field}")

        # --------------------------------
        # Validate title
        # --------------------------------

        title = adapter.get("title")

        if not isinstance(title, str) or not title.strip():
            raise DropItem("Invalid title")

        # --------------------------------
        # Validate URL
        # --------------------------------

        url = adapter.get("url")

        if not is_valid_url(url):
            raise DropItem(f"Invalid URL: {url}")

        # --------------------------------
        # Validate UPC
        # --------------------------------

        upc = adapter.get("upc")

        if not isinstance(upc, str) or not upc.strip():
            raise DropItem("Invalid UPC")

        # --------------------------------
        # Validate numeric types
        # --------------------------------

        numeric_fields = [
            "price",
            "price_excl_tax",
            "price_incl_tax",
            "tax",
            "rating",
            "number_of_reviews",
        ]

        for field in numeric_fields:
            value = adapter.get(field)

            if value is not None and not isinstance(value, (int, float)):
                raise DropItem(f"Invalid {field} type: {type(value).__name__}")

        # --------------------------------
        # Validate price
        # --------------------------------

        price = adapter.get("price")

        if price is not None and price < 0:
            raise DropItem(f"Invalid price: {price}")

        # --------------------------------
        # Validate price excluding tax
        # --------------------------------

        price_excl_tax = adapter.get("price_excl_tax")

        if price_excl_tax is not None and price_excl_tax < 0:
            raise DropItem(f"Invalid price_excl_tax: {price_excl_tax}")

        # --------------------------------
        # Validate price including tax
        # --------------------------------

        price_incl_tax = adapter.get("price_incl_tax")

        if price_incl_tax is not None and price_incl_tax < 0:
            raise DropItem(f"Invalid price_incl_tax: {price_incl_tax}")

        # --------------------------------
        # Validate price relationship
        # --------------------------------

        if (
            price_excl_tax is not None
            and price_incl_tax is not None
            and price_incl_tax < price_excl_tax
        ):
            raise DropItem(
                f"Invalid price relationship: "
                f"incl={price_incl_tax}, "
                f"excl={price_excl_tax}"
            )

        # --------------------------------
        # Validate tax
        # --------------------------------

        tax = adapter.get("tax")

        if tax is not None and tax < 0:
            raise DropItem(f"Invalid tax: {tax}")

        # --------------------------------
        # Validate rating
        # --------------------------------

        rating = adapter.get("rating")

        if rating is not None and not 1 <= rating <= 5:
            raise DropItem(f"Invalid rating: {rating}")

        # --------------------------------
        # Validate number of reviews
        # --------------------------------

        number_of_reviews = adapter.get("number_of_reviews")

        if number_of_reviews is not None and number_of_reviews < 0:
            raise DropItem(f"Invalid reviews: {number_of_reviews}")

        return item


class DuplicateBookPipeline:

    def __init__(self):
        self.seen_upcs = set()

    def process_item(self, item):

        if not isinstance(item, BookcrawlerItem):
            return item

        adapter = ItemAdapter(item)

        upc = adapter.get("upc")

        if upc:
            if upc in self.seen_upcs:
                raise DropItem(f"Duplicate book: {upc}")

            self.seen_upcs.add(upc)

        return item


class DataQualityPipeline:

    def __init__(self):
        self.dropped_items = 0
        self.drop_reasons = {}

    def process_item(self, item):
        return item

    def close_spider(self, spider):
        spider.logger.info("========== DATA QUALITY REPORT ==========")
        spider.logger.info(
            "Items dropped: %s",
            self.dropped_items,
        )

        for reason, count in self.drop_reasons.items():
            spider.logger.info(
                "%s: %s",
                reason,
                count,
            )

        spider.logger.info("========================================")


class QuoteValidationPipeline:

    def process_item(self, item):

        if not isinstance(item, QuoteItem):
            return item

        if not item.text:
            raise DropItem("Missing quote text")

        if not item.author:
            raise DropItem("Missing quote author")

        return item


class JobValidationPipeline:
    def process_item(self, item):
        if not isinstance(item, JobItem):
            return item

        if not item.title or not item.title.strip():
            raise DropItem("Job missing title")

        if not item.url or not item.url.startswith(("http://", "https://")):
            raise DropItem(f"Invalid job URL: {item.url}")

        if not item.source or not item.source.strip():
            raise DropItem("Job missing source")

        if not item.external_id or not item.external_id.strip():
            raise DropItem("Job missing external_id")

        if not item.scraped_at:
            raise DropItem("Job missing scraped_at")

        if item.remote is not None and not isinstance(item.remote, bool):
            raise DropItem("Invalid remote value")

        return item


class JobDeduplicationPipeline:
    def __init__(self):
        self.seen_jobs = set()

    def process_item(self, item):
        if not isinstance(item, JobItem):
            return item

        key = (item.source, item.external_id)

        if key in self.seen_jobs:
            raise DropItem(
                f"Duplicate job: source={item.source}, "
                f"external_id={item.external_id}"
            )

        self.seen_jobs.add(key)

        return item
