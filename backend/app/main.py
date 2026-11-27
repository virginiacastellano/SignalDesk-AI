from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging, logger
from app.infrastructure.database.session import create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("service.starting", environment=settings.environment)
    if settings.environment == "development":
        await create_database()
    yield
    logger.info("service.stopped")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="SaaS multi-tenant para automatizacion de WhatsApp con IA.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["system"])
async def root():
    return {"name": settings.app_name, "docs": "/docs", "health": f"{settings.api_v1_prefix}/health"}
