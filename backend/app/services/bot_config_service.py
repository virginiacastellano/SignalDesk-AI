from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.bot_config import BotConfig
from app.domain.schemas.bot_config import BotConfigUpdate


class BotConfigService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, tenant_id: str) -> BotConfig:
        config = await self.session.scalar(select(BotConfig).where(BotConfig.tenant_id == tenant_id))
        if config:
            return config
        config = BotConfig(tenant_id=tenant_id)
        self.session.add(config)
        await self.session.commit()
        await self.session.refresh(config)
        return config

    async def update(self, tenant_id: str, payload: BotConfigUpdate) -> BotConfig:
        config = await self.get_or_create(tenant_id)
        for field, value in payload.model_dump().items():
            setattr(config, field, value)
        await self.session.commit()
        await self.session.refresh(config)
        return config
