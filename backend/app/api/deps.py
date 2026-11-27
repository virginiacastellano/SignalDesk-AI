from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import PermissionDeniedError
from app.core.security import decode_access_token
from app.domain.models.tenant import Membership, User
from app.infrastructure.database.session import get_session

bearer = HTTPBearer()


async def get_current_identity(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    payload = decode_access_token(credentials.credentials)
    user = await session.get(User, payload["sub"])
    if not user or not user.is_active:
        raise PermissionDeniedError("Usuario inactivo o inexistente")
    membership = await session.scalar(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.tenant_id == payload["tenant_id"],
        )
    )
    if not membership:
        raise PermissionDeniedError("El usuario no pertenece a este tenant")
    return {"user": user, "tenant_id": membership.tenant_id, "role": membership.role}
