from app.models.loan import AmortizationSchedule
from app.repositories.base import BaseRepository


class AmortizationScheduleRepository(BaseRepository[AmortizationSchedule]):
    model = AmortizationSchedule
