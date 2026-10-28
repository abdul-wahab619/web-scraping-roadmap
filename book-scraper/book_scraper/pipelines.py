import os
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

import psycopg
from dotenv import load_dotenv
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

load_dotenv()


class PostgresPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self):
        """Connect to PostgreSQL and prepare the database table."""
        spider = self.crawler.spider

        self.connection = psycopg.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "book_scraper_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD"),
            connect_timeout=10,
        )

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title TEXT NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                rating SMALLINT NOT NULL
                    CHECK (rating BETWEEN 1 AND 5),
                in_stock BOOLEAN NOT NULL,
                stock_count INTEGER NOT NULL DEFAULT 0
                    CHECK (stock_count >= 0),
                product_url TEXT NOT NULL UNIQUE,
                image_url TEXT,
                scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        self.connection.commit()

        if spider:
            spider.logger.info("Connected to PostgreSQL.")

    def process_item(self, item):
        spider = self.crawler.spider
        """Validate and upsert one book record."""

        adapter = ItemAdapter(item)

        title = adapter.get("title")
        product_url = adapter.get("product_url")
        image_url = adapter.get("image_url")
        rating = adapter.get("rating")
        price = adapter.get("price")
        availability = adapter.get("availability")

        if not isinstance(title, str) or not title.strip():
            raise DropItem("Missing book title")

        if not isinstance(product_url, str) or not product_url.strip():
            raise DropItem(f"Missing product URL: {title}")

        if not isinstance(availability, dict):
            raise DropItem(f"Invalid availability: {title}")

        if type(rating) is not int or not 1 <= rating <= 5:
            raise DropItem(f"Invalid rating: {title}")

        try:
            price = Decimal(str(price))
        except (InvalidOperation, ValueError, TypeError):
            raise DropItem(f"Invalid price: {title}")

        if not price.is_finite() or price <= 0 or price >= Decimal("100000000"):
            raise DropItem(f"Price outside supported range: {title}")

        if price.as_tuple().exponent < -2:
            raise DropItem(f"Price has more than two decimals: {title}")

        in_stock = availability.get("in_stock")
        stock_count = availability.get("stock_count")

        if type(in_stock) is not bool:
            raise DropItem(f"Invalid stock status: {title}")

        if type(stock_count) is not int or stock_count < 0:
            raise DropItem(f"Invalid stock count: {title}")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO books (
                        title,
                        price,
                        rating,
                        in_stock,
                        stock_count,
                        product_url,
                        image_url,
                        scraped_at,
                        updated_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (product_url)
                    DO UPDATE SET
                        title = EXCLUDED.title,
                        price = EXCLUDED.price,
                        rating = EXCLUDED.rating,
                        in_stock = EXCLUDED.in_stock,
                        stock_count = EXCLUDED.stock_count,
                        image_url = EXCLUDED.image_url,
                        scraped_at = EXCLUDED.scraped_at,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        title.strip(),
                        price,
                        rating,
                        in_stock,
                        stock_count,
                        product_url,
                        image_url,
                        datetime.now(timezone.utc),
                        datetime.now(timezone.utc),
                    ),
                )

            self.connection.commit()

        except psycopg.Error:
            self.connection.rollback()
            if spider:
                spider.logger.exception(
                    "PostgreSQL write failed for %s",
                    product_url,
                )
            raise

        return item

    def close_spider(self):
        """Close the database connection when crawling ends."""
        spider = self.crawler.spider

        if getattr(self, "connection", None) is not None:
            self.connection.close()
            if spider:
                spider.logger.info("PostgreSQL connection closed.")
