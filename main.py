from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import (
    SessionLocal,
    check_redis_connection,
    engine,
    get_db,
    initDB,
    redis_client,
)
from models import Notice
from scraper import run_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    check_redis_connection()

    db = SessionLocal()
    try:
        run_scraper(redis_client=redis_client, db=db)
    finally:
        db.close()

    yield

    engine.dispose()
    print("Application shutting down")


app = FastAPI(title="TU NOTICE TRACKER", lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "API is operational."}


class NoticesModel(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


@app.get("/notices")
def notices(
    pasignation: Annotated[NoticesModel, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    total = db.query(Notice).count()

    notices = (
        db.query(Notice)
        .order_by(Notice.notice_id.desc())
        .offset((pasignation.page - 1) * pasignation.page_size)
        .limit(pasignation.page_size)
        .all()
    )
    return {
        "page": pasignation.page,
        "page_size": pasignation.page_size,
        "total": total,
        "total_pages": (total + pasignation.page_size - 1) // pasignation.page_size,
        "notices": notices,
    }
