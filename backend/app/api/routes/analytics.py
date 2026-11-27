from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.domain.schemas.analytics import DashboardMetrics
from app.infrastructure.database.session import get_session
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard", response_model=DashboardMetrics)
async def dashboard(identity: Annotated[dict, Depends(get_current_identity)], session: Annotated[AsyncSession, Depends(get_session)]):
    return await AnalyticsService(session).dashboard(identity["tenant_id"])
