from datetime import datetime
from uuid import UUID, uuid4
from enum import StrEnum

from sqlalchemy import DateTime, Enum, Index, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from tracker.shared.database import Base

class ApplicationStatus(StrEnum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    DELETED = "deleted"


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    position: Mapped[str] = mapped_column(String(200))
    company: Mapped[str | None] = mapped_column(String(200), default=None)
    link: Mapped[str] = mapped_column(String(2000))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(
            ApplicationStatus,
            native_enum=False,
            length=20
        ),
        default=ApplicationStatus.APPLIED,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )