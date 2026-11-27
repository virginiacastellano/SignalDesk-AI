from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.infrastructure.database.session import get_session
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, session: Annotated[AsyncSession, Depends(get_session)]):
    return await AuthService(session).register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: Annotated[AsyncSession, Depends(get_session)]):
    return await AuthService(session).login(payload)
