from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TenantRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def list(self, tenant_id: str, limit: int = 100):
        result = await self.session.scalars(
            select(self.model).where(self.model.tenant_id == tenant_id).limit(limit)
        )
        return list(result)

    async def add(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
