from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.auth import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> User | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[User]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: UserCreate, actor_id: UUID | None = None) -> User:
        if await self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if await self.repo.get_by_username(payload.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        data = payload.model_dump(exclude={"password"})
        entity = User(
            **data,
            hashed_password=get_password_hash(payload.password),
            created_by=actor_id,
            updated_by=actor_id,
        )
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: UserUpdate, actor_id: UUID | None = None) -> User | None:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return None
        data = payload.model_dump(exclude_unset=True)
        password = data.pop("password", None)
        if password:
            data["hashed_password"] = get_password_hash(password)
        return await self.repo.update(entity, data, updated_by=actor_id)

    async def delete(self, entity_id: UUID) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return False
        await self.repo.delete(entity)
        return True
