from datetime import UTC, datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.analytics import DailyMetric
from app.domain.models.automation import Workflow, WorkflowRun
from app.domain.models.bot_config import BotConfig
from app.domain.models.conversation import Conversation, Message
from app.domain.models.integration import Integration
from app.domain.models.lead import Lead


class DemoService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def reset(self, tenant_id: str) -> dict:
        for model in [Message, Conversation, Lead, WorkflowRun, Workflow, Integration, DailyMetric, BotConfig]:
            await self.session.execute(delete(model).where(model.tenant_id == tenant_id))

        lead = Lead(
            tenant_id=tenant_id,
            name="Valentina Rios",
            phone="+5491138429910",
            tags=["enterprise", "hot lead"],
            score=86,
        )
        self.session.add(lead)
        await self.session.flush()

        conversation = Conversation(
            tenant_id=tenant_id,
            lead_id=lead.id,
            bot_enabled=True,
            status="open",
            last_message_at=datetime.now(UTC),
        )
        self.session.add(conversation)
        await self.session.flush()

        self.session.add_all(
            [
                Message(tenant_id=tenant_id, conversation_id=conversation.id, direction="inbound", sender_type="lead", content="Hola, quiero automatizar WhatsApp para mi equipo comercial.", status="received"),
                Message(tenant_id=tenant_id, conversation_id=conversation.id, direction="outbound", sender_type="bot", content="Perfecto. Puedo ayudarte a calificar leads, responder FAQs y derivar casos importantes al equipo.", status="sent"),
                Workflow(tenant_id=tenant_id, name="Lead qualification", trigger="message.received", conditions={"intent": "pricing"}, actions=[{"type": "tag", "value": "hot lead"}]),
                Workflow(tenant_id=tenant_id, name="Human handoff", trigger="handoff.detected", conditions={}, actions=[{"type": "assign_team", "team": "sales"}]),
                Integration(tenant_id=tenant_id, provider="google_sheets", status="connected"),
                Integration(tenant_id=tenant_id, provider="gmail", status="ready"),
                Integration(tenant_id=tenant_id, provider="crm_webhook", status="connected"),
                BotConfig(tenant_id=tenant_id),
            ]
        )
        await self.session.commit()
        return {"status": "reset", "tenant_id": tenant_id}
