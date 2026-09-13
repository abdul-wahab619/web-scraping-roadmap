import subprocess

from redis_client import redis_client
from datetime import datetime, timezone

MAX_RETRIES = 1

SCRAPY_PROJECT_DIR = r"D:\web-scraping-roadmap\scrapy_projects\bookcrawler"

SCRAPY_PYTHON = (
    r"D:\web-scraping-roadmap\scrapy_projects" r"\bookcrawler\.venv\Scripts\python.exe"
)


def process_job(job_id):
    job_key = f"scrape_job:{job_id}"

    attempt = int(redis_client.hget(job_key, "attempt") or 0) + 1

    redis_client.hset(
        job_key,
        "attempt",
        attempt,
    )
    started_at = datetime.now(timezone.utc).isoformat()

    print(f"Processing job: {job_id} (attempt {attempt})")

    redis_client.hset(
        job_key,
        mapping={
            "status": "running",
            "started_at": started_at,
        },
    )

    try:
        subprocess.run(
            [
                SCRAPY_PYTHON,
                "-m",
                "scrapy",
                "crawl",
                "books",
            ],
            cwd=SCRAPY_PROJECT_DIR,
            check=True,
        )

        completed_at = datetime.now(timezone.utc).isoformat()

        started = datetime.fromisoformat(redis_client.hget(job_key, "started_at"))

        completed = datetime.fromisoformat(completed_at)

        duration_seconds = (completed - started).total_seconds()

        redis_client.hset(
            job_key,
            mapping={
                "status": "completed",
                "completed_at": completed_at,
                "duration_seconds": duration_seconds,
            },
        )

        print(f"Completed job: {job_id}")

    except Exception as error:
        failed_at = datetime.now(timezone.utc).isoformat()

        started = datetime.fromisoformat(redis_client.hget(job_key, "started_at"))

        failed = datetime.fromisoformat(failed_at)

        duration_seconds = (failed - started).total_seconds()

        if attempt <= MAX_RETRIES:
            redis_client.hset(
                job_key,
                mapping={
                    "status": "retrying",
                    "error": str(error),
                    "failed_at": failed_at,
                    "duration_seconds": duration_seconds,
                },
            )

            redis_client.lpush(
                "scrape_queue",
                job_id,
            )

            print(f"Job failed. Retrying: {job_id}")

        else:
            redis_client.hset(
                job_key,
                mapping={
                    "status": "failed",
                    "error": str(error),
                    "failed_at": failed_at,
                    "duration_seconds": duration_seconds,
                },
            )

            print(f"Job failed permanently: {job_id}")
            print(f"Error: {error}")


def start_worker():
    print("Worker started. Waiting for jobs...")

    while True:
        result = redis_client.brpop(
            "scrape_queue",
            timeout=5,
        )

        if result is None:
            continue

        _, job_id = result

        process_job(job_id)


if __name__ == "__main__":
    start_worker()
