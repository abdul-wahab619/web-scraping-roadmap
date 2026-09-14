# import os
import time
import logging
import uuid
from datetime import datetime, timezone, timedelta

# from dotenv import load_dotenv

from redis_client import redis_client

# load_dotenv()

# SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", "60"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def get_scrape_interval():
    interval = redis_client.hget(
        "scrape_schedule",
        "interval_seconds",
    )

    if interval is None:
        return 60

    return int(interval)


def create_scrape_job():
    lock_key = "scrape_scheduler_lock"
    interval = get_scrape_interval()

    lock_acquired = redis_client.set(
        lock_key,
        "1",
        nx=True,
        ex=max(interval * 2, 60),
    )

    if not lock_acquired:
        logger.warning(
            "A scheduled scrape is already running. " "Skipping this schedule."
        )
        return

    job_id = str(uuid.uuid4())

    job_key = f"scrape_job:{job_id}"

    scheduled_at = datetime.now(timezone.utc).isoformat()

    next_run_at = (datetime.now(timezone.utc) + timedelta(seconds=interval)).isoformat()

    redis_client.hset(
        job_key,
        mapping={
            "job_id": job_id,
            "status": "queued",
            "job_type": "scheduled",
            "scheduled_at": scheduled_at,
            "next_run_at": next_run_at,
        },
    )

    redis_client.lpush(
        "scrape_queue",
        job_id,
    )
    redis_client.hset(
        "scrape_schedule",
        "last_run_at",
        scheduled_at,
    )

    logger.info(f"Scheduled scrape job: {job_id}")


def start_scheduler():
    logger.info("Scheduler started.")

    while True:
        try:
            interval = get_scrape_interval()

            logger.info(f"Next scrape interval: {interval} seconds")

            create_scrape_job()

        except Exception as error:
            logger.error(f"Scheduler error: {error}")

            interval = 10

        time.sleep(interval)


if __name__ == "__main__":
    start_scheduler()
