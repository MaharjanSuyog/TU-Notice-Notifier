import random
import time
from datetime import datetime
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup
from models import Notice, Tag
from redis import Redis
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.classify import classify

BASE_URL = "https://iost.tu.edu.np"
NOTICES_URL = f"{BASE_URL}/notices"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

REDIS_RECENT_NAME = "recent_notices_ids"

MAX_PAGES = 10
KNOWN_THRESHOLD = 3
REDIS_CACHE_SIZE = 20


def get_notice_id(href: str):
    return int(href.rstrip("/").split("/")[-1])


def fetch_posts(url):
    resp = httpx.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    notices = []
    for notice in soup.select(".recent-post-wrapper"):
        title_tag = notice.select_one("h5")
        link_tag = notice.select_one("a")
        date_tag = notice.select_one("span")

        if not all([title_tag, link_tag, date_tag]):
            continue

        href = link_tag.get("href")
        if not href:
            continue

        full_href = urljoin(BASE_URL, href)
        notices.append(
            {
                "id": get_notice_id(full_href),
                "title": title_tag.get_text(strip=True),
                "href": href,
                "date": date_tag.get_text(strip=True),
            }
        )
    return notices, soup


def get_next_page_url(soup, current_url):
    next_link = soup.find("a", string="Next »")
    if not next_link:
        return None

    href = next_link.get("href")
    if not href:
        return None

    return urljoin(current_url, href)


def get_cached_notices_ids(redis_client: Redis) -> set[str]:
    return set(redis_client.lrange(REDIS_RECENT_NAME, 0, -1))


def cache_notice_id(redis_client: Redis, notice_id: int):
    notice_id = str(notice_id)

    redis_client.lrem(REDIS_RECENT_NAME, 0, notice_id)
    redis_client.lpush(REDIS_RECENT_NAME, notice_id)

    redis_client.ltrim(REDIS_RECENT_NAME, 0, REDIS_CACHE_SIZE - 1)


def get_existing_notice_ids(db: Session, notice_ids: list[list]) -> set[int]:
    if not notice_ids:
        return set()

    rows = db.query(Notice.notice_id).filter(Notice.notice_id.in_(notice_ids)).all()

    return {row[0] for row in rows}


def save_new_notices(redis_client: Redis, db: Session, notices: list[dict]):
    if not notices:
        return []

    saved_posts = []

    for item in notices:
        tag_names = classify(item["title"])

        tags = []
        if tag_names:
            tags = (
                db.execute(select(Tag).where(Tag.name.in_(tag_names))).scalars().all()
            )

        notice = Notice(
            notice_id=item["id"],
            title=item["title"],
            href=item["href"],
            published_date=datetime.strptime(item["date"], "%Y-%m-%d").replace(
                tzinfo=ZoneInfo("Asia/Kathmandu")
            ),
            tags=tags,
        )
        try:
            db.add(notice)
            db.commit()
            db.refresh(Notice)
            cache_notice_id(redis_client, item["id"])

            saved_posts.append(notice)

            print(f"Saved new notice: {item['id']} - {item['title']}")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Failed to save notice: {item['id']} - {item['title']}: {e}")
    return saved_posts


def get_new_notices(redis_client: Redis, db: Session):
    url = NOTICES_URL
    new_notices = []
    known_count = 0
    pages_fetched = 0

    while url and pages_fetched < MAX_PAGES:
        print(
            f"{datetime.now(tz=ZoneInfo('Asia/Kathmandu')).strftime('%Y-%m-%d %H:%M')}: Fetching {url}"
        )
        try:
            notices, soup = fetch_posts(url)
            cached_ids = get_cached_notices_ids(redis_client)
            redis_miss_posts = []
            for notice in notices:
                notice_id = str(notice["id"])

                if str(notice_id) in cached_ids:
                    known_count += 1
                    continue
                redis_miss_posts.append(notice)

            redis_miss_ids = [notice["id"] for notice in redis_miss_posts]
            existing_db_ids = get_existing_notice_ids(db, redis_miss_ids)

            for notice in redis_miss_posts:
                notice_id = notice["id"]

                if notice_id in existing_db_ids:
                    known_count += 1
                else:
                    new_notices.append(notice)

            if known_count >= KNOWN_THRESHOLD:
                break

            time.sleep(random.uniform(1.0, 2.0))
            url = get_next_page_url(soup, url)

            pages_fetched += 1

        except httpx.HTTPError as e:
            print(
                f"Fetch failed at {url}: {e} — stopping this run, keeping notices found so far"
            )
            break
    return new_notices


def run_scraper(redis_client: Redis, db: Session):
    print("Starting notice scraper")
    new_notices = get_new_notices(redis_client, db)

    if not new_notices:
        print("No new notices found")
        return []

    saved_posts = save_new_notices(redis_client, db, new_notices)

    print(f"Saved {len(saved_posts)} new notice(s)")
    return saved_posts
