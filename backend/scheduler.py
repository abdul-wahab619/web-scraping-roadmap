# import os
import time
import logging
import uuid
from datetime import datetime, timezone, timedelta
from database import get_connection

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


def get_enabled_sources():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT source
                FROM sources
                WHERE enabled = TRUE
                ORDER BY source
                """)

            rows = cursor.fetchall()

            return [row[0] for row in rows]

    finally:
        connection.close()


def get_source_eligibility(source: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    s.enabled,
                    s.interval_minutes,

                    EXISTS (
                        SELECT 1
                        FROM crawl_runs running
                        WHERE running.source = s.source
                          AND running.status = 'running'
                    ) AS crawl_running,

                    MAX(cr.started_at) AS latest_crawl

                FROM sources s

                LEFT JOIN crawl_runs cr
                    ON cr.source = s.source

                WHERE s.source = %s

                GROUP BY
                    s.source,
                    s.enabled,
                    s.interval_minutes
                """,
                (source,),
            )

            row = cursor.fetchone()

            if row is None:
                return {
                    "eligible": False,
                    "reason": "SOURCE_NOT_FOUND",
                }

            enabled, interval_minutes, crawl_running, latest_crawl = row

            if not enabled:
                return {
                    "eligible": False,
                    "reason": "DISABLED",
                }

            if crawl_running:
                return {
                    "eligible": False,
                    "reason": "ALREADY_RUNNING",
                }

            if latest_crawl is not None:
                cooldown_until = latest_crawl + timedelta(minutes=interval_minutes)

                now = datetime.now(timezone.utc)

                if now < cooldown_until:
                    return {
                        "eligible": False,
                        "reason": "COOLDOWN",
                    }

            return {
                "eligible": True,
                "reason": "ELIGIBLE",
            }

    finally:
        connection.close()


def create_scrape_job(source: str):
    eligibility = get_source_eligibility(source)

    if not eligibility["eligible"]:
        logger.info(
            "Skipping source '%s': %s",
            source,
            eligibility["reason"],
        )
        return

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
            "source": source,
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

    logger.info(
        "Scheduled scrape job: %s for source '%s'",
        job_id,
        source,
    )


def start_scheduler():
    logger.info("Scheduler started.")

    while True:
        try:
            interval = get_scrape_interval()

            logger.info(
                "Next scrape interval: %s seconds",
                interval,
            )

            sources = get_enabled_sources()

            logger.info(
                "Found %d enabled source(s): %s",
                len(sources),
                sources,
            )

            for source in sources:
                create_scrape_job(source)

        except Exception as error:
            logger.exception(
                "Scheduler error: %s",
                error,
            )

            interval = 10

        time.sleep(interval)


if __name__ == "__main__":
    start_scheduler()
