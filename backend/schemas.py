from datetime import datetime
from pydantic import BaseModel


class SourceHealth(BaseModel):
    source: str
    latest_crawl_id: int
    latest_status: str

    latest_items_found: int
    latest_items_dropped: int

    latest_requests: int
    latest_responses: int
    latest_retries: int
    latest_http_errors: int
    latest_spider_exceptions: int

    latest_duration: float | None
    latest_finished_at: datetime | None

    avg_items_found: float | None
    percentage_of_average: float | None

    health: str

    last_successful_crawl: datetime | None

    failed_crawls: int
    consecutive_failures: int

    latest_duration_seconds: float | None
    avg_duration_seconds: float | None
    duration_percentage_of_average: float | None

    latest_error_message: str | None


class CrawlRun(BaseModel):
    id: int
    source: str
    started_at: datetime
    finished_at: datetime | None

    status: str
    items_found: int
    items_dropped: int

    requests: int
    responses: int
    retries: int
    http_errors: int
    spider_exceptions: int

    error_message: str | None


class Book(BaseModel):
    id: int
    title: str
    price: float | None = None
    rating: int | None = None
    url: str
    upc: str
    product_type: str | None = None
    price_excl_tax: float | None = None
    price_incl_tax: float | None = None
    tax: float | None = None
    availability: str | None = None
    number_of_reviews: int | None = None
    description: str | None = None


class BooksResponse(BaseModel):
    count: int
    limit: int
    offset: int
    books: list[Book]
