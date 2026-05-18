from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loan import RiskAssessment
from app.repositories.risk_assessment_repository import RiskAssessmentRepository


class RiskAssessmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = RiskAssessmentRepository(session)
        self.session = session

    async def get(self, entity_id: UUID) -> RiskAssessment | None:
        return await self.repo.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 50) -> list[RiskAssessment]:
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self) -> int:
        return await self.repo.count()
