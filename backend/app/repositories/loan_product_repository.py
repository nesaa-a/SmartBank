from app.models.loan import LoanProduct
from app.repositories.base import BaseRepository


class LoanProductRepository(BaseRepository[LoanProduct]):
    model = LoanProduct
