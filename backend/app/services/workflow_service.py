from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.automation import Workflow
from app.domain.schemas.workflow import WorkflowCreate
from app.infrastructure.repositories.base import TenantRepository


class WorkflowService:
    def __init__(self, session: AsyncSession):
        self.repo = TenantRepository(session, Workflow)

    async def list(self, tenant_id: str):
        return await self.repo.list(tenant_id)

    async def create(self, tenant_id: str, payload: WorkflowCreate):
        return await self.repo.add(Workflow(tenant_id=tenant_id, **payload.model_dump()))
