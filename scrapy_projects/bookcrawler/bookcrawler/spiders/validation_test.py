import scrapy
from datetime import datetime, timezone

from bookcrawler.items import JobItem


class ValidationTestSpider(scrapy.Spider):
    name = "validation_test"

    async def start(self):
        yield scrapy.Request(
            url="data:text/plain,test",
            callback=self.parse,
        )

    def parse(self, response):
        self.logger.info("TEST SPIDER: parse() executed")

        yield JobItem(
            title=None,
            company="Test Company",
            location="Remote",
            job_type="Full-time",
            remote=True,
            salary=None,
            description="Test job",
            url="https://example.com/job/123",
            source="test",
            external_id="123",
            posted_at=None,
            scraped_at=datetime.now(timezone.utc).isoformat(),
        )
