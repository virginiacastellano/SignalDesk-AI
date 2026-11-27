from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.security import Role, create_access_token, hash_password, verify_password
from app.domain.models.tenant import Membership, Tenant, User
from app.domain.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        existing = await self.session.scalar(select(User).where(User.email == payload.email))
        if existing:
            raise AppError("Ya existe un usuario con ese email")

        tenant = Tenant(name=payload.company_name, slug=payload.company_slug)
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        membership = Membership(tenant=tenant, user=user, role=Role.OWNER.value)
        self.session.add_all([tenant, user, membership])
        await self.session.commit()
        await self.session.refresh(user)
        token = create_access_token(user.id, tenant.id, Role.OWNER.value)
        return TokenResponse(access_token=token, tenant_id=tenant.id, role=Role.OWNER.value, user={"email": user.email, "name": user.full_name})

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.session.scalar(select(User).where(User.email == payload.email))
        if not user or not verify_password(payload.password, user.hashed_password):
            raise AppError("Credenciales invalidas")

        membership = await self.session.scalar(select(Membership).where(Membership.user_id == user.id))
        if not membership:
            raise AppError("Usuario sin tenant asociado")

        token = create_access_token(user.id, membership.tenant_id, membership.role)
        return TokenResponse(access_token=token, tenant_id=membership.tenant_id, role=membership.role, user={"email": user.email, "name": user.full_name})
