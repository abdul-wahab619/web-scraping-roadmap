import scrapy
from datetime import datetime, timezone
from urllib.parse import urlparse

from bookcrawler.items import JobItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    source_name = "ycombinator"

    allowed_domains = [
        "news.ycombinator.com",
        "ycombinator.com",
    ]

    def start_requests(self):
        yield scrapy.Request(
            url="https://news.ycombinator.com/jobs",
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/153.0.0.0 Safari/537.36"
                )
            },
            callback=self.parse,
        )

    start_urls = [
        "https://news.ycombinator.com/jobs",
    ]

    def parse(self, response):
        yc_job_urls = response.css(
            "a[href^='https://www.ycombinator.com/companies/']"
            "[href*='/jobs/']::attr(href)"
        ).getall()

        self.logger.info(
            "Found %d YC job URLs",
            len(yc_job_urls),
        )

        for url in yc_job_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_job,
            )

    def parse_job(self, response):
        title = response.css("h1.ycdc-section-title::text").get()

        company = response.css("h2.text-2xl a::text").get()

        metadata = response.css("h1.ycdc-section-title + div span::text").getall()

        salary = metadata[0] if len(metadata) > 0 else None
        location = metadata[4] if len(metadata) > 4 else None

        job_type = response.xpath(
            "//strong[normalize-space()='Job type']"
            "/../following-sibling::span[1]/text()"
        ).get()

        remote = "Remote" in location if location else False

        description = (
            response.xpath(
                "//h2[contains(@class, 'ycdc-section-title') "
                "and normalize-space(.)='About the role']"
                "/following-sibling::div[1]"
                "//div[contains(@class, 'prose')]"
            )
            .xpath("string(.)")
            .get()
        )

        path = urlparse(response.url).path
        job_slug = path.rstrip("/").split("/")[-1]

        external_id = job_slug.split("-", 1)[0]

        yield JobItem(
            title=title.strip() if title else None,
            company=company.strip() if company else None,
            location=location.strip() if location else None,
            job_type=job_type.strip() if job_type else None,
            remote=remote,
            salary=salary.strip() if salary else None,
            description=(description.strip() if description else None),
            url=response.url,
            source="ycombinator",
            external_id=external_id,
            posted_at=None,
            scraped_at=datetime.now(timezone.utc).isoformat(),
        )
