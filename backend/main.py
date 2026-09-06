import os
from contextlib import asynccontextmanager

import httpx
from database import (
    SessionLocal,
    check_redis_connection,
    engine,
    get_db,
    initDB,
    redis_client,
)
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, notices
from scraper import run_scraper

load_dotenv()

BREVO_API_URL = os.getenv("BREVO_API_URL")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "TU NOTIFIER")


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    check_redis_connection()
    # mail("test-bfd9tb81h@srv1.mail-tester.com", "HELLO", "https://youtube.com")
    # db = SessionLocal()
    # try:
    #     run_scraper(redis_client=redis_client, db=db)
    # finally:
    #     db.close()

    yield

    engine.dispose()
    print("Application shutting down")


app = FastAPI(title="TU NOTICE TRACKER", lifespan=lifespan, redirect_slashes=False)


@app.get("/")
def home():
    return {"message": "API is operational."}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notices.router)
app.include_router(auth.router)

# @app.get("/web")
# def web():
#     httpx.post(
#         "https://discord.com/api/webhooks/1545747401925722202/VYMcNe_POvTsloqaDTcPznVxlr4xGnA5C7w0GNpr5QUWQz-yZB0naDA_DCh3NhSzMm2C",
#         json={
#             "embeds": [
#                 {
#                     "title": "weeeeee",
#                     "url": "https://localhost:3000",
#                     "color": "3447003",
#                 }
#             ]
#         },
#     )


def mail(to_email: str, notice_title: str, notice_link: str) -> dict:
    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": f"New IOST notice: {notice_title}",
        "htmlContent": f"""
            <p>A new notice was published on IOST's notice board:</p>
            <p><strong>{notice_title}</strong></p>
            <p><a href="{notice_link}">Read the full notice</a></p>
            <p style="color:#888;font-size:12px">
                You're receiving this because you subscribed to Sanket.
            </p>
        """,
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    response = httpx.post(BREVO_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
