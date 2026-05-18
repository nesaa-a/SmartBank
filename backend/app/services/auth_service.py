import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.auth import RefreshToken, User, UserRole
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import TokenResponse

settings = get_settings()


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)
        self.role_repo = RoleRepository(session)

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    async def register(self, payload: RegisterRequest) -> User:
        if await self.user_repo.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if await self.user_repo.get_by_username(payload.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        user = User(
            email=payload.email,
            username=payload.username,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            is_active=payload.is_active,
            is_superuser=payload.is_superuser,
        )
        user = await self.user_repo.create(user)

        default_role = await self.role_repo.get_by_name("analyst")
        if default_role:
            user_role = UserRole(
                user_id=user.id,
                role_id=default_role.id,
                created_by=user.id,
                updated_by=user.id,
            )
            self.session.add(user_role)
            await self.session.flush()
        return user

    async def login(self, payload: LoginRequest, device_info: str | None = None) -> TokenResponse:
        user = await self.user_repo.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
        return await self._issue_tokens(user, device_info)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        token_hash = self._hash_token(refresh_token)
        stored = await self.refresh_repo.get_by_hash(token_hash)
        if stored is None or stored.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
        if stored.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        user = await self.user_repo.get_by_id(stored.user_id)
        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        await self.refresh_repo.revoke(stored)
        return await self._issue_tokens(user, stored.device_info)

    async def logout(self, refresh_token: str) -> None:
        token_hash = self._hash_token(refresh_token)
        stored = await self.refresh_repo.get_by_hash(token_hash)
        if stored and stored.revoked_at is None:
            await self.refresh_repo.revoke(stored)

    async def _issue_tokens(self, user: User, device_info: str | None = None) -> TokenResponse:
        jti = str(uuid.uuid4())
        refresh_token = create_refresh_token(user.id, jti)
        access_token = create_access_token(user.id)

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        refresh_entity = RefreshToken(
            user_id=user.id,
            token_hash=self._hash_token(refresh_token),
            expires_at=expires_at,
            device_info=device_info,
            created_by=user.id,
            updated_by=user.id,
        )
        await self.refresh_repo.create(refresh_entity)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
