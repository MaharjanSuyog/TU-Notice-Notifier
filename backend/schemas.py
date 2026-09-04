from datetime import datetime

from models import Notice
from pydantic import BaseModel, ConfigDict


class NoticeOut(BaseModel):
    notice_id: int
    title: str
    href: str
    published_date: datetime
    tags: list[str]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_notice(cls, notice: Notice) -> "NoticeOut":
        return cls(
            notice_id=notice.notice_id,
            title=notice.title,
            href=notice.href,
            published_date=notice.published_date,
            tags=[t.name for t in notice.tags] if notice.tags else ["notice"],
        )
