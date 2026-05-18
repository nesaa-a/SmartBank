from app.models.loan import Repayment
from app.repositories.base import BaseRepository


class RepaymentRepository(BaseRepository[Repayment]):
    model = Repayment
