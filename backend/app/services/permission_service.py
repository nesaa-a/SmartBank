from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import Permission
from app.repositories.permission_repository import PermissionRepository
from app.schemas.auth import PermissionResponse
from app.schemas.auth import PermissionCreate
from app.schemas.auth import PermissionUpdate

class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = PermissionRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> Permission | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[Permission]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: PermissionCreate, actor_id: UUID | None = None) -> Permission:
        entity = Permission(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: PermissionUpdate, actor_id: UUID | None = None) -> Permission | None:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return None
        return await self.repo.update(entity, payload.model_dump(exclude_unset=True), updated_by=actor_id)

    async def delete(self, entity_id: UUID) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return False
        await self.repo.delete(entity)
        return True
