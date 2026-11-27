from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.models.conversation import Conversation, Message
from app.domain.models.lead import Lead
from app.core.errors import NotFoundError
from app.infrastructure.providers.openai_provider import AIProvider
from app.infrastructure.providers.whatsapp_provider import WhatsAppProvider
from app.services.bot_config_service import BotConfigService


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ai = AIProvider()
        self.whatsapp = WhatsAppProvider()
        self.bot_config_service = BotConfigService(session)

    async def list_conversations(self, tenant_id: str) -> list[Conversation]:
        result = await self.session.scalars(
            select(Conversation)
            .where(Conversation.tenant_id == tenant_id)
            .options(selectinload(Conversation.messages))
            .order_by(desc(Conversation.last_message_at))
            .limit(50)
        )
        return list(result)

    async def send_agent_message(self, *, tenant_id: str, conversation_id: str, content: str, recipient_phone: str) -> Message:
        conversation = await self.session.scalar(
            select(Conversation).where(Conversation.id == conversation_id, Conversation.tenant_id == tenant_id)
        )
        if not conversation:
            raise NotFoundError("Conversacion no encontrada")

        await self.whatsapp.send_text(to=recipient_phone, body=content)
        now = datetime.now(UTC)
        message = Message(
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            direction="outbound",
            sender_type="agent",
            content=content,
            status="sent",
        )
        conversation.last_message_at = now
        if conversation.status == "needs_human":
            conversation.status = "open"
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def ingest_inbound_whatsapp(self, *, tenant_id: str, phone: str, text: str, external_id: str | None = None) -> Message:
        lead = await self.session.scalar(select(Lead).where(Lead.tenant_id == tenant_id, Lead.phone == phone))
        if not lead:
            lead = Lead(tenant_id=tenant_id, name=f"Lead {phone[-4:]}", phone=phone, tags=["inbound"])
            self.session.add(lead)
            await self.session.flush()

        conversation = await self.session.scalar(
            select(Conversation).options(selectinload(Conversation.messages)).where(
                Conversation.tenant_id == tenant_id,
                Conversation.lead_id == lead.id,
                Conversation.status.in_(["open", "needs_human"]),
            )
        )
        if not conversation:
            conversation = Conversation(tenant_id=tenant_id, lead_id=lead.id, last_message_at=datetime.now(UTC))
            self.session.add(conversation)
            await self.session.flush()

        inbound = Message(
            tenant_id=tenant_id,
            conversation_id=conversation.id,
            external_id=external_id,
            direction="inbound",
            sender_type="lead",
            content=text,
            status="received",
        )
        self.session.add(inbound)

        if conversation.bot_enabled:
            bot_config = await self.bot_config_service.get_or_create(tenant_id)
            previous_messages = await self.session.scalars(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at)
                .limit(12)
            )
            history = [
                {"role": "assistant" if msg.sender_type in {"bot", "agent"} else "user", "content": msg.content}
                for msg in previous_messages
            ]
            ai = self._configured_reply(bot_config, text)
            outbound = Message(
                tenant_id=tenant_id,
                conversation_id=conversation.id,
                direction="outbound",
                sender_type="bot",
                content=ai["reply"],
                status="queued",
                meta={
                    "intent": ai["intent"],
                    "handoff_required": ai["handoff_required"],
                    "interactive": ai.get("interactive"),
                },
            )
            self.session.add(outbound)
            if ai["handoff_required"]:
                conversation.bot_enabled = False
                conversation.status = "needs_human"

        conversation.last_message_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(inbound)
        return inbound

    async def handle_interactive_reply(
        self,
        *,
        tenant_id: str,
        conversation_id: str,
        option_id: str,
        option_title: str,
    ) -> Message:
        conversation = await self.session.scalar(
            select(Conversation).where(Conversation.id == conversation_id, Conversation.tenant_id == tenant_id)
        )
        if not conversation:
            raise NotFoundError("Conversacion no encontrada")

        now = datetime.now(UTC)
        inbound = Message(
            tenant_id=tenant_id,
            conversation_id=conversation.id,
            direction="inbound",
            sender_type="lead",
            content=option_title,
            status="received",
            meta={"interactive_reply": {"id": option_id, "title": option_title}},
        )
        self.session.add(inbound)

        bot_config = await self.bot_config_service.get_or_create(tenant_id)
        reply = self._reply_for_option(bot_config, option_id)
        outbound = Message(
            tenant_id=tenant_id,
            conversation_id=conversation.id,
            direction="outbound",
            sender_type="bot",
            content=reply["content"],
            status="queued",
            meta={"intent": reply["intent"], "handoff_required": reply["handoff_required"], "interactive": reply.get("interactive")},
        )
        self.session.add(outbound)

        conversation.last_message_at = now
        if reply["handoff_required"]:
            conversation.bot_enabled = False
            conversation.status = "needs_human"

        await self.session.commit()
        await self.session.refresh(outbound)
        return outbound

    async def _touch_conversation(self, conversation_id: str) -> None:
        conversation = await self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.last_message_at = datetime.now(UTC)

    def _configured_reply(self, bot_config, user_message: str) -> dict:
        lower_message = user_message.lower()
        if any(keyword.lower() in lower_message for keyword in bot_config.handoff_keywords):
            reply = self._reply_for_option(bot_config, "human")
            return {
                "reply": reply["content"],
                "intent": reply["intent"],
                "handoff_required": reply["handoff_required"],
                "interactive": reply.get("interactive"),
            }

        if any(keyword.lower() in lower_message for keyword in bot_config.menu_keywords):
            return {
                "reply": bot_config.welcome_message,
                "intent": "main_menu",
                "handoff_required": False,
                "interactive": {
                    "type": "list",
                    "title": bot_config.menu_title,
                    "button": bot_config.menu_button_label,
                    "sections": bot_config.menu_sections,
                },
            }

        return {
            "reply": bot_config.fallback_message,
            "intent": "fallback",
            "handoff_required": False,
            "interactive": {
                "type": "buttons",
                "buttons": [
                    {"id": "pricing", "title": "Ver planes"},
                    {"id": "demo", "title": "Agendar demo"},
                    {"id": "human", "title": "Asesor"},
                ],
            },
        }

    def _reply_for_option(self, bot_config, option_id: str) -> dict:
        reply = bot_config.option_replies.get(
            option_id,
            {
                "content": "Gracias. Tome tu seleccion y puedo seguir ayudandote desde aca.",
                "intent": "interactive_reply",
                "handoff_required": False,
            },
        )
        return {
            "content": reply["content"],
            "intent": reply.get("intent", f"{option_id}_selected"),
            "handoff_required": reply.get("handoff_required", False),
            "interactive": reply.get("interactive"),
        }
