from app.models.loan import ApprovedLoan
from app.repositories.base import BaseRepository


class ApprovedLoanRepository(BaseRepository[ApprovedLoan]):
    model = ApprovedLoan
