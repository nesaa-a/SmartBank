from app.models.loan import UnderwritingLog
from app.repositories.base import BaseRepository


class UnderwritingLogRepository(BaseRepository[UnderwritingLog]):
    model = UnderwritingLog
