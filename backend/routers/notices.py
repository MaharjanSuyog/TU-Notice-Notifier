from typing import Annotated

from database import get_db
from fastapi import APIRouter, Depends, Response
from models import Notice, Tag
from pydantic import BaseModel, Field
from schemas import NoticeOut
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

router = APIRouter(prefix="/notices", tags=["notices"])


class NoticesModel(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    tag: str | None = None
    tags: str | None = None


@router.get("")
def notices(
    pasignation: Annotated[NoticesModel, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    query = db.query(Notice).options(selectinload(Notice.tags))

    if pasignation.tag:
        query = query.join(Notice.tags).filter(Tag.name == pasignation.tag)
    elif pasignation.tags:
        tag_list = [t.strip() for t in pasignation.tags.split(",") if t.strip()]
        query = (
            query.join(Notice.tags)
            .filter(Tag.name.in_(tag_list))
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


@router.get("/tags")
def list_tags(db: Annotated[Session, Depends(get_db)], response: Response):
    used = (
        db.query(Tag.kind, Tag.name)
        .join(Notice.tags)
        .distinct()
        .order_by(Tag.kind, Tag.name)
        .all()
    )
    tags = {}
    for kind, name in used:
        tags.setdefault(kind, []).append(name)

    response.headers["Cache-Control"] = "public, max-age=3600"
    return {"tags": tags}
