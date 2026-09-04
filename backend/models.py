from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()

notice_tags = Table(
    "notice_tags",
    Base.metadata,
    Column(
        "notice_id",
        UUID,
        ForeignKey("notices.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    notices: Mapped[list["Notice"]] = relationship(
        secondary=notice_tags, back_populates="tags"
    )


class Notice(Base):
    __tablename__ = "notices"

    id: Mapped[str] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )
    notice_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    href: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    published_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=ZoneInfo("Asia/Kathmandu")),
    )
    tags: Mapped[list["Tag"]] = relationship(
        secondary=notice_tags, back_populates="notices"
    )
