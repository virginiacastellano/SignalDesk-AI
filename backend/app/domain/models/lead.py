from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    lifecycle_stage: Mapped[str] = mapped_column(String(40), default="new")
    source: Mapped[str] = mapped_column(String(80), default="whatsapp")
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    score: Mapped[int] = mapped_column(default=50)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
