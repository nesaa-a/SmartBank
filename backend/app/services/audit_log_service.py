from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.system import AuditLogResponse
from app.schemas.system import AuditLogCreate

class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AuditLogRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> AuditLog | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[AuditLog]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: AuditLogCreate, actor_id: UUID | None = None) -> AuditLog:
        entity = AuditLog(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def delete(self, entity_id: UUID) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return False
        await self.repo.delete(entity)
        return True
