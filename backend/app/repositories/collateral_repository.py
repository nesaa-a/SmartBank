from app.models.loan import Collateral
from app.repositories.base import BaseRepository


class CollateralRepository(BaseRepository[Collateral]):
    model = Collateral
