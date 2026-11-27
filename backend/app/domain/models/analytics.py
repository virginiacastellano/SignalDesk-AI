from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class DailyMetric(Base):
    __tablename__ = "daily_metrics"
    __table_args__ = (UniqueConstraint("tenant_id", "metric_date", name="uq_metric_tenant_date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    metric_date: Mapped[date] = mapped_column(Date, index=True)
    inbound_messages: Mapped[int] = mapped_column(default=0)
    outbound_messages: Mapped[int] = mapped_column(default=0)
    ai_resolutions: Mapped[int] = mapped_column(default=0)
    human_handoffs: Mapped[int] = mapped_column(default=0)
    new_leads: Mapped[int] = mapped_column(default=0)
    conversions: Mapped[int] = mapped_column(default=0)
    avg_first_response_seconds: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
