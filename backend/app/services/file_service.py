from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system import File
from app.repositories.file_repository import FileRepository
from app.schemas.system import FileResponse
from app.schemas.system import FileCreate

class FileService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = FileRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> File | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[File]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: FileCreate, actor_id: UUID | None = None) -> File:
        entity = File(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def delete(self, entity_id: UUID) -> bool:
        entity = await self.repo.get_by_id(entity_id)
        if entity is None:
            return False
        await self.repo.delete(entity)
        return True
