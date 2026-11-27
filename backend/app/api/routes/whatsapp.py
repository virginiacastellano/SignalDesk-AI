from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.core.config import settings
from app.domain.schemas.whatsapp import (
    WhatsAppInteractiveReplyRequest,
    WhatsAppSimulationRequest,
    WhatsAppTemplateMessage,
    WhatsAppTextMessage,
)
from app.infrastructure.database.session import get_session
from app.infrastructure.providers.whatsapp_provider import WhatsAppProvider
from app.services.conversation_service import ConversationService

router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_challenge: str = Query(alias="hub.challenge"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return int(hub_challenge)
    return {"error": "invalid_verify_token"}


@router.post("/webhook")
async def receive_webhook(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    payload = await request.json()
    tenant_id = payload.get("tenant_id")
    entries = payload.get("entry", [])
    if not tenant_id:
        tenant_id = await _first_tenant_id(session)
    for entry in entries:
        for change in entry.get("changes", []):
            for message in change.get("value", {}).get("messages", []):
                text = message.get("text", {}).get("body", "")
                phone = message.get("from", "")
                if text and phone and tenant_id:
                    await ConversationService(session).ingest_inbound_whatsapp(
                        tenant_id=tenant_id,
                        phone=phone,
                        text=text,
                        external_id=message.get("id"),
                    )
    return {"received": True}


@router.post("/messages/text")
async def send_text(payload: WhatsAppTextMessage, _: Annotated[dict, Depends(get_current_identity)]):
    return await WhatsAppProvider().send_text(to=payload.to, body=payload.body)


@router.post("/messages/template")
async def send_template(payload: WhatsAppTemplateMessage, _: Annotated[dict, Depends(get_current_identity)]):
    return await WhatsAppProvider().send_template(
        to=payload.to,
        template_name=payload.template_name,
        language_code=payload.language_code,
        components=payload.components,
    )


@router.post("/simulate")
async def simulate_inbound_message(
    payload: WhatsAppSimulationRequest,
    identity: Annotated[dict, Depends(get_current_identity)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    message = await ConversationService(session).ingest_inbound_whatsapp(
        tenant_id=identity["tenant_id"],
        phone=payload.phone,
        text=payload.message,
        external_id=f"sim-{payload.phone}-{payload.message[:16]}",
    )
    return {"received": True, "message_id": message.id}


@router.post("/interactive-reply")
async def interactive_reply(
    payload: WhatsAppInteractiveReplyRequest,
    identity: Annotated[dict, Depends(get_current_identity)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    message = await ConversationService(session).handle_interactive_reply(
        tenant_id=identity["tenant_id"],
        conversation_id=payload.conversation_id,
        option_id=payload.option_id,
        option_title=payload.option_title,
    )
    return {"received": True, "message_id": message.id}


async def _first_tenant_id(session: AsyncSession) -> str | None:
    from app.domain.models.tenant import Tenant

    return await session.scalar(select(Tenant.id).limit(1))
