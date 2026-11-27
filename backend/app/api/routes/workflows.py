from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.domain.schemas.workflow import WorkflowCreate, WorkflowRead
from app.infrastructure.database.session import get_session
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.get("", response_model=list[WorkflowRead])
async def list_workflows(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await WorkflowService(session).list(identity["tenant_id"])


@router.post("", response_model=WorkflowRead)
async def create_workflow(payload: WorkflowCreate, identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await WorkflowService(session).create(identity["tenant_id"], payload)
