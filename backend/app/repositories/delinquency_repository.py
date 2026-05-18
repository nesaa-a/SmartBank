from app.models.loan import Delinquency
from app.repositories.base import BaseRepository


class DelinquencyRepository(BaseRepository[Delinquency]):
    model = Delinquency
