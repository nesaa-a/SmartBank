from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loan import LoanApplication
from app.repositories.loan_application_repository import LoanApplicationRepository
from app.schemas.loan import LoanApplicationResponse
from app.schemas.loan import LoanApplicationCreate
from app.schemas.loan import LoanApplicationUpdate

class LoanApplicationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = LoanApplicationRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> LoanApplication | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[LoanApplication]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: LoanApplicationCreate, actor_id: UUID | None = None) -> LoanApplication:
        entity = LoanApplication(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: LoanApplicationUpdate, actor_id: UUID | None = None) -> LoanApplication | None:
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
