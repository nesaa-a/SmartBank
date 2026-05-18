from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loan import CreditScore
from app.repositories.credit_score_repository import CreditScoreRepository
from app.schemas.loan import CreditScoreResponse
from app.schemas.loan import CreditScoreCreate
from app.schemas.loan import CreditScoreUpdate

class CreditScoreService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = CreditScoreRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> CreditScore | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[CreditScore]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: CreditScoreCreate, actor_id: UUID | None = None) -> CreditScore:
        entity = CreditScore(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: CreditScoreUpdate, actor_id: UUID | None = None) -> CreditScore | None:
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
