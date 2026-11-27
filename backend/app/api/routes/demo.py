from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.infrastructure.database.session import get_session
from app.services.demo_service import DemoService

router = APIRouter()


@router.post("/reset")
async def reset_demo(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await DemoService(session).reset(identity["tenant_id"])
