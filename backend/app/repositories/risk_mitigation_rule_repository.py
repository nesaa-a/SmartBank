from app.models.loan import RiskMitigationRule
from app.repositories.base import BaseRepository


class RiskMitigationRuleRepository(BaseRepository[RiskMitigationRule]):
    model = RiskMitigationRule
