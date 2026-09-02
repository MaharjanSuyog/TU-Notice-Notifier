from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import UUID, Column, DateTime, Integer, String, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Notice(Base):
    __tablename__ = "notices"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    notice_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    href = Column(String, nullable=False, unique=True)
    published_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=ZoneInfo("Asia/Kathmandu")),
    )
