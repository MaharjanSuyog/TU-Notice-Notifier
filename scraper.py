from datetime import datetime
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup
from redis import Redis

BASE_URL = "https://iost.tu.edu.np"
NOTICES_URL = f"{BASE_URL}/notices"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

MAX_PAGES = 10
KNOWN_THRESHOLD = 3


def get_notice_id(href: str):
    return href.rstrip("/").split("/")[-1]


def fetch_posts(url):
    resp = httpx.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    posts = []
    for post in soup.select(".recent-post-wrapper"):
        title_tag = post.select_one("h5")
        link_tag = post.select_one("a")
        date_tag = post.select_one("span")

        if not all([title_tag, link_tag, date_tag]):
            continue

        href = link_tag.get("href")
        if not href:
            continue

        posts.append(
            {
                "id": get_notice_id(href),
                "title": title_tag.get_text(strip=True),
                "href": href,
                "date": date_tag.get_text(strip=True),
            }
        )
    return posts, soup


def get_next_page_url(soup, current_url):
    next_link = soup.find("a", string="Next »")
    print(next_link)
    if not next_link:
        return None

    href = next_link.get("href")
    if not href:
        return None

    return urljoin(current_url, next_link)


def get_new_notices(redis_client: Redis):
    url = NOTICES_URL
    new_posts = []
    known_count = 0
    pages_fetched = 0

    while url and pages_fetched < MAX_PAGES:
        print(
            f"{datetime.now(tz=ZoneInfo('Asia/Kathmandu')).strftime('%Y-%m-%d %H:%M')}: Fetching {url}"
        )

        posts, soup = fetch_posts(NOTICES_URL)
        for post in posts:
            notice_id = post["id"]

            if redis_client.sismember("recent_notices_ids", notice_id):
                known_count += 1
            else:
                new_posts.append(post)

            if known_count >= KNOWN_THRESHOLD:
                return new_posts

            url = get_next_page_url(soup, url)

            pages_fetched += 1

        return new_posts


# _, soup = fetch_posts(URL)
# get_next_page_url(soup, URL)
# print(get_notice_id("https://iost.tu.edu.np/notices/14813"))
get_new_notices()
