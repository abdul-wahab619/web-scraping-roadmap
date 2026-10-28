from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet import reactor
from twisted.internet.task import deferLater


class RetryAfterMiddleware(RetryMiddleware):
    """Honor Retry-After for HTTP 429 responses."""

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler.settings)
        middleware.crawler = crawler
        return middleware

    def process_response(self, request, response):
        spider = self.crawler.spider

        if response.status != 429:
            return super().process_response(request, response)

        retry_after = response.headers.get("Retry-After")

        if not retry_after:
            return super().process_response(request, response)

        value = retry_after.decode("ascii", errors="ignore").strip()

        try:
            delay = max(0.0, float(value))
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(value)

                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)

                delay = max(
                    0.0,
                    (retry_at - datetime.now(timezone.utc)).total_seconds(),
                )
            except (TypeError, ValueError, OverflowError):
                return super().process_response(request, response)

        retry_request = super().process_response(request, response)

        if not isinstance(retry_request, request.__class__):
            return retry_request
        if spider:
            spider.logger.warning(
                "HTTP 429: delaying retry for %.1f seconds: %s",
                delay,
                request.url,
            )

        deferred = deferLater(
            reactor,
            delay,
            lambda: retry_request,
        )
        return deferred
