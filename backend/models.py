import enum
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


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

subscriber_category_tags = Table(
    "subscriber_category_tags",
    Base.metadata,
    Column(
        "subscriber_id",
        UUID,
        ForeignKey("subscribers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class TagKind(str, enum.Enum):
    PROGRAM = "program"
    SEMESTER = "semester"
    CATEGORY = "category"
    MODIFIER = "modifier"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    kind: Mapped[TagKind] = mapped_column(
        Enum(
            TagKind,
            name="tag_kind",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        server_default=TagKind.MODIFIER.value,
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


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[str] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    google_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    status: Mapped[str] = mapped_column(String, default="active")
    unsubscribe_token: Mapped[str] = mapped_column(
        String, unique=True, server_default=text("gen_random_uuid()")
    )
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=ZoneInfo("Asia/Kathmandu")),
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    program_tag_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tags.id", ondelete="SET NULL"), nullable=True
    )
    program_tag: Mapped[Tag | None] = relationship(foreign_keys=[program_tag_id])

    semester_tag_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tags.id", ondelete="SET NULL"), nullable=True
    )
    semester_tag: Mapped[Tag | None] = relationship(foreign_keys=[semester_tag_id])

    category_tags: Mapped[list[Tag]] = relationship(
        secondary=subscriber_category_tags, lazy="selectin"
    )

    @property
    def onboarding_complete(self) -> bool:
        return (
            self.program_tag_id is not None
            and self.semester_tag_id is not None
            and len(self.category_tags) > 0
        )
