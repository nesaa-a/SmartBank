from app.models.loan import Guarantor
from app.repositories.base import BaseRepository


class GuarantorRepository(BaseRepository[Guarantor]):
    model = Guarantor
