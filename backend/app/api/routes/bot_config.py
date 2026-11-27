from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.domain.schemas.bot_config import BotConfigRead, BotConfigUpdate
from app.infrastructure.database.session import get_session
from app.services.bot_config_service import BotConfigService

router = APIRouter()


@router.get("", response_model=BotConfigRead)
async def get_bot_config(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await BotConfigService(session).get_or_create(identity["tenant_id"])


@router.put("", response_model=BotConfigRead)
async def update_bot_config(payload: BotConfigUpdate, identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await BotConfigService(session).update(identity["tenant_id"], payload)
