from datetime import UTC, datetime, timedelta
from enum import StrEnum

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import PermissionDeniedError


class Role(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    AGENT = "agent"
    ANALYST = "analyst"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, tenant_id: str, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "tenant_id": tenant_id, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise PermissionDeniedError("Token invalido o expirado") from exc


def ensure_role(current_role: str, allowed: set[Role]) -> None:
    if Role(current_role) not in allowed:
        raise PermissionDeniedError("No tenes permisos para esta accion")
