from fastapi import APIRouter

from app.api.routes import analytics, auth, bot_config, conversations, demo, health, integrations, leads, whatsapp, workflows

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(bot_config.router, prefix="/bot-config", tags=["bot-config"])
api_router.include_router(demo.router, prefix="/demo", tags=["demo"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
