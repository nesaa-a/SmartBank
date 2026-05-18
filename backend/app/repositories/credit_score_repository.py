from uuid import UUID

from sqlalchemy import select

from app.models.loan import CreditScore
from app.repositories.base import BaseRepository


class CreditScoreRepository(BaseRepository[CreditScore]):
    model = CreditScore

    async def get_latest_by_customer(self, customer_id: UUID) -> CreditScore | None:
        stmt = (
            select(CreditScore)
            .where(CreditScore.customer_id == customer_id)
            .order_by(CreditScore.report_date.desc(), CreditScore.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
