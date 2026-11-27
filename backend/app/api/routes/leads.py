from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.domain.models.lead import Lead
from app.domain.schemas.lead import LeadCreate, LeadRead
from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.base import TenantRepository

router = APIRouter()


@router.get("", response_model=list[LeadRead])
async def list_leads(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await TenantRepository(session, Lead).list(identity["tenant_id"])


@router.post("", response_model=LeadRead)
async def create_lead(payload: LeadCreate, identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await TenantRepository(session, Lead).add(Lead(tenant_id=identity["tenant_id"], **payload.model_dump()))
