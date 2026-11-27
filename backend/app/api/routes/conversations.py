from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.domain.schemas.conversation import ConversationRead, MessageCreate, MessageRead
from app.infrastructure.database.session import get_session
from app.services.conversation_service import ConversationService

router = APIRouter()


@router.get("", response_model=list[ConversationRead])
async def list_conversations(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await ConversationService(session).list_conversations(identity["tenant_id"])


@router.post("/messages", response_model=MessageRead)
async def send_message(payload: MessageCreate, identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await ConversationService(session).send_agent_message(
        tenant_id=identity["tenant_id"],
        conversation_id=payload.conversation_id,
        content=payload.content,
        recipient_phone=payload.recipient_phone or "",
    )
