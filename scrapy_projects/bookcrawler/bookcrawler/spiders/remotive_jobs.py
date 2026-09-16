import scrapy
from datetime import datetime, timezone

from bookcrawler.items import JobItem


class RemotiveJobsSpider(scrapy.Spider):
    name = "remotive_jobs"

    allowed_domains = [
        "remotive.com",
    ]

    async def start(self):
        yield scrapy.Request(
            url="https://remotive.com/api/remote-jobs",
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()

        jobs = data.get("jobs", [])

        self.logger.info(
            "Remotive returned %d jobs",
            len(jobs),
        )

        for job in jobs:
            crawl_time = datetime.now(timezone.utc).isoformat()

            yield JobItem(
                title=job.get("title", "").strip() or None,
                company=job.get("company_name", "").strip() or None,
                location=job.get("candidate_required_location", "").strip() or None,
                job_type=job.get("job_type", "").strip() or None,
                remote=True,
                salary=job.get("salary", "").strip() or None,
                description=job.get("description", "").strip() or None,
                url=job.get("url"),
                source="remotive",
                external_id=str(job.get("id")),
                posted_at=job.get("publication_date"),
                last_seen_at=crawl_time,
                scraped_at=crawl_time,
            )
