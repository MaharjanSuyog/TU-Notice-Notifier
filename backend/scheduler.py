import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database import SessionLocal, redis_client
from scraper import run_scraper

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

SCRAPE_INTERVAL_MINUTES = 5


async def scheduled_scrape_job():
    db = SessionLocal()
    try:
        await run_scraper(redis_client=redis_client, db=db)
    except Exception:
        logger.exception("Scheduled scrape failed")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        scheduled_scrape_job,
        trigger=IntervalTrigger(minutes=SCRAPE_INTERVAL_MINUTES),
        id="scrape_notices",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60,
    )

    scheduler.start()


def stop_scheduler():
    scheduler.shutdown(wait=False)
