from uuid import UUID

from sqlalchemy import select

from app.models.loan import FinancialProfile
from app.repositories.base import BaseRepository


class FinancialProfileRepository(BaseRepository[FinancialProfile]):
    model = FinancialProfile

    async def get_latest_by_customer(self, customer_id: UUID) -> FinancialProfile | None:
        stmt = (
            select(FinancialProfile)
            .where(FinancialProfile.customer_id == customer_id)
            .order_by(FinancialProfile.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
