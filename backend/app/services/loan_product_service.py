from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loan import LoanProduct
from app.repositories.loan_product_repository import LoanProductRepository
from app.schemas.loan import LoanProductResponse
from app.schemas.loan import LoanProductCreate
from app.schemas.loan import LoanProductUpdate

class LoanProductService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = LoanProductRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> LoanProduct | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[LoanProduct]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()

    async def create(self, payload: LoanProductCreate, actor_id: UUID | None = None) -> LoanProduct:
        entity = LoanProduct(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)
        return await self.repo.create(entity)

    async def update(self, entity_id: UUID, payload: LoanProductUpdate, actor_id: UUID | None = None) -> LoanProduct | None:
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
