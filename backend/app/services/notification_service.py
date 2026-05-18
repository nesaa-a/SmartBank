from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system import Notification
from app.repositories.notification_repository import NotificationRepository
from app.schemas.system import NotificationResponse
from app.schemas.system import NotificationCreate
from app.schemas.system import NotificationUpdate

class NotificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = NotificationRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> Notification | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[Notification]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: NotificationCreate, actor_id: UUID | None = None) -> Notification:
        entity = Notification(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: NotificationUpdate, actor_id: UUID | None = None) -> Notification | None:
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
