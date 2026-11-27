from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.conversation import Conversation, Message
from app.domain.models.lead import Lead
from app.domain.schemas.analytics import DashboardMetrics


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def dashboard(self, tenant_id: str) -> DashboardMetrics:
        active_conversations = await self.session.scalar(
            select(func.count()).select_from(Conversation).where(Conversation.tenant_id == tenant_id, Conversation.status.in_(["open", "needs_human"]))
        )
        total_leads = await self.session.scalar(select(func.count()).select_from(Lead).where(Lead.tenant_id == tenant_id))
        outbound = await self.session.scalar(select(func.count()).select_from(Message).where(Message.tenant_id == tenant_id, Message.direction == "outbound"))
        bot = await self.session.scalar(select(func.count()).select_from(Message).where(Message.tenant_id == tenant_id, Message.sender_type == "bot"))
        messages = await self.session.scalar(select(func.count()).select_from(Message).where(Message.tenant_id == tenant_id))
        return DashboardMetrics(
            active_conversations=active_conversations or 0,
            total_leads=total_leads or 0,
            conversion_rate=18.6,
            ai_resolution_rate=round(((bot or 0) / max(outbound or 1, 1)) * 100, 1),
            avg_response_seconds=42,
            messages_today=messages or 0,
            revenue_pipeline=42800,
            bot_health="operational",
        )
