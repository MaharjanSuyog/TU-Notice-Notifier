import httpx
from bs4 import BeautifulSoup

URL = "https://iost.tu.edu.np/notices"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


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

        posts.append(
            {
                "title": title_tag.get_text(strip=True),
                "href": link_tag.get("href"),
                "date": date_tag.get_text(strip=True),
            }
        )
    return posts
