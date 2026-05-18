from app.models.loan import RiskAssessment
from app.repositories.base import BaseRepository


class RiskAssessmentRepository(BaseRepository[RiskAssessment]):
    model = RiskAssessment
