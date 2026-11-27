import asyncio

from sqlalchemy import select

from app.core.security import Role, hash_password
from app.domain.models.automation import Workflow
from app.domain.models.bot_config import BotConfig
from app.domain.models.conversation import Conversation, Message
from app.domain.models.integration import Integration
from app.domain.models.lead import Lead
from app.domain.models.tenant import Membership, Tenant, User
from app.infrastructure.database.session import SessionLocal, create_database


async def main() -> None:
    await create_database()
    async with SessionLocal() as session:
        tenant = await session.scalar(select(Tenant).where(Tenant.slug == "nova-growth"))
        if tenant:
            return

        tenant = Tenant(name="Nova Growth Studio", slug="nova-growth", industry="B2B Services")
        user = User(email="founder@novagrowth.io", full_name="Alex Founder", hashed_password=hash_password("Password123!"))
        session.add_all([tenant, user])
        await session.flush()

        membership = Membership(tenant_id=tenant.id, user_id=user.id, role=Role.OWNER.value)
        lead = Lead(tenant_id=tenant.id, name="Valentina Rios", phone="+5491138429910", tags=["enterprise", "hot lead"], score=86)
        session.add_all([membership, lead])
        await session.flush()

        conversation = Conversation(tenant_id=tenant.id, lead_id=lead.id, bot_enabled=True, status="open")
        workflows = [
            Workflow(tenant_id=tenant.id, name="Lead qualification", trigger="message.received", conditions={"intent": "pricing"}, actions=[{"type": "tag", "value": "hot lead"}]),
            Workflow(tenant_id=tenant.id, name="Human handoff", trigger="handoff.detected", actions=[{"type": "assign_team", "team": "sales"}]),
        ]
        integrations = [
            Integration(tenant_id=tenant.id, provider="google_sheets", status="connected"),
            Integration(tenant_id=tenant.id, provider="gmail", status="ready"),
            Integration(tenant_id=tenant.id, provider="crm_webhook", status="connected"),
        ]
        session.add_all([conversation, *workflows, *integrations, BotConfig(tenant_id=tenant.id)])
        await session.flush()
        session.add_all(
            [
                Message(tenant_id=tenant.id, conversation_id=conversation.id, direction="inbound", sender_type="lead", content="Hola, quiero automatizar WhatsApp para mi equipo comercial.", status="received"),
                Message(tenant_id=tenant.id, conversation_id=conversation.id, direction="outbound", sender_type="bot", content="Perfecto. Puedo ayudarte a calificar leads, responder FAQs y derivar casos importantes al equipo.", status="sent"),
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
