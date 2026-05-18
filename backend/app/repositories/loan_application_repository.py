from sqlalchemy import select

from app.models.loan import LoanApplication
from app.repositories.base import BaseRepository


class LoanApplicationRepository(BaseRepository[LoanApplication]):
    model = LoanApplication

    async def get_by_application_number(self, application_number: str) -> LoanApplication | None:
        stmt = select(LoanApplication).where(LoanApplication.application_number == application_number)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
