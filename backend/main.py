from contextlib import asynccontextmanager
from typing import Annotated

from database import (
    SessionLocal,
    check_redis_connection,
    engine,
    get_db,
    initDB,
    redis_client,
)
from fastapi import Depends, FastAPI
from models import Notice, Tag
from pydantic import BaseModel, Field
from schemas import NoticeOut
from scraper import run_scraper
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    check_redis_connection()

    db = SessionLocal()
    # try:
    #     run_scraper(redis_client=redis_client, db=db)
    # finally:
    #     db.close()

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
    tag: str | None = None
    tags: str | None = None


@app.get("/notices")
def notices(
    pasignation: Annotated[NoticesModel, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    query = db.query(Notice).options(selectinload(Notice.tags))

    if pasignation.tag:
        query = query.join(Notice.tags).filter(Tag.name == pasignation.tag)
    elif pasignation.tags:
        tag_list = [t.strip() for t in pasignation.tags.split(",") if t.strip()]
        query = query.join(Notice.tags).filter(
            Tag.name.in_(tag_list)
            .group_by(Notice.id)
            .having(func.count(func.distinct(Tag.id)) == len(tag_list))
        )

    total = query.count()

    notices = (
        query.order_by(Notice.notice_id.desc())
        .offset((pasignation.page - 1) * pasignation.page_size)
        .limit(pasignation.page_size)
        .all()
    )
    return {
        "page": pasignation.page,
        "page_size": pasignation.page_size,
        "total": total,
        "total_pages": (total + pasignation.page_size - 1) // pasignation.page_size,
        "notices": [NoticeOut.from_notice(n) for n in notices],
    }


@app.get("/tags")
def list_tags(db: Annotated[Session, Depends(get_db)]):
    used = db.query(Tag.name).join(Notice.tags).distinct().order_by(Tag.name).all()
    return {"tags": [t[0] for t in used]}
