from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.websocket import websocket_manager
from app.models.loan import LoanApplication, LoanApplicationStatus, RiskAssessment, RiskLevel
from app.models.system import AuditLog, Notification
from app.repositories.credit_score_repository import CreditScoreRepository
from app.repositories.financial_profile_repository import FinancialProfileRepository
from app.repositories.loan_application_repository import LoanApplicationRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.risk_assessment_repository import RiskAssessmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.loan import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    LoanApplicationWithRiskResponse,
)


class LoanService:
    MODEL_VERSION = "mock-v1"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.application_repo = LoanApplicationRepository(session)
        self.financial_repo = FinancialProfileRepository(session)
        self.credit_repo = CreditScoreRepository(session)
        self.risk_repo = RiskAssessmentRepository(session)
        self.notification_repo = NotificationRepository(session)
        self.user_repo = UserRepository(session)

    async def create_application(
        self,
        payload: LoanApplicationCreate,
        actor_id: UUID,
    ) -> LoanApplicationWithRiskResponse:
        existing = await self.application_repo.get_by_application_number(payload.application_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application number already exists",
            )

        application = LoanApplication(
            **payload.model_dump(),
            status=LoanApplicationStatus.SUBMITTED,
            submitted_at=datetime.now(timezone.utc),
            created_by=actor_id,
            updated_by=actor_id,
        )
        application = await self.application_repo.create(application)

        financial_profile = await self.financial_repo.get_latest_by_customer(payload.customer_id)
        credit_score = await self.credit_repo.get_latest_by_customer(payload.customer_id)

        risk_score, factors = self._evaluate_risk_score(
            application=application,
            financial_profile=financial_profile,
            credit_score=credit_score,
        )
        risk_level = self._map_risk_level(risk_score)

        assessment = RiskAssessment(
            loan_application_id=application.id,
            risk_level=risk_level,
            risk_score=risk_score,
            model_version=self.MODEL_VERSION,
            factors=factors,
            assessed_at=datetime.now(timezone.utc),
            created_by=actor_id,
            updated_by=actor_id,
        )
        assessment = await self.risk_repo.create(assessment)

        audit = AuditLog(
            user_id=actor_id,
            action="loan_application_created",
            entity_type="loan_application",
            entity_id=application.id,
            details={"risk_level": risk_level.value, "risk_score": risk_score},
            created_by=actor_id,
            updated_by=actor_id,
        )
        self.session.add(audit)

        if risk_level == RiskLevel.HIGH:
            await self._notify_high_risk(application, assessment, actor_id)
            await websocket_manager.broadcast_json(
                {
                    "event": "high_risk_application",
                    "application_id": str(application.id),
                    "application_number": application.application_number,
                    "customer_id": str(application.customer_id),
                    "risk_level": risk_level.value,
                    "risk_score": risk_score,
                    "factors": factors,
                },
                channel="risk_alerts",
            )

        base = LoanApplicationResponse.model_validate(application)
        return LoanApplicationWithRiskResponse(
            **base.model_dump(),
            risk_assessment=assessment,
        )

    def _evaluate_risk_score(self, application, financial_profile, credit_score) -> tuple[int, dict]:
        risk_score = 0
        factors: dict = {}

        if credit_score is None:
            risk_score += 25
            factors["credit_score"] = {"points": 25, "reason": "missing_credit_score"}
        elif credit_score.score < 600:
            risk_score += 40
            factors["credit_score"] = {"points": 40, "score": credit_score.score, "reason": "below_600"}
        elif credit_score.score < 650:
            risk_score += 20
            factors["credit_score"] = {"points": 20, "score": credit_score.score, "reason": "below_650"}

        if financial_profile is None:
            risk_score += 20
            factors["financial_profile"] = {"points": 20, "reason": "missing_financial_profile"}
        else:
            dti = float(financial_profile.debt_to_income_ratio)
            if dti > 0.43:
                risk_score += 30
                factors["debt_to_income"] = {"points": 30, "dti": dti, "reason": "above_0_43"}
            elif dti > 0.36:
                risk_score += 15
                factors["debt_to_income"] = {"points": 15, "dti": dti, "reason": "above_0_36"}

            annual_income = float(financial_profile.annual_income)
            if annual_income > 0 and float(application.requested_amount) > annual_income * 0.5:
                risk_score += 25
                factors["loan_to_income"] = {
                    "points": 25,
                    "requested_amount": float(application.requested_amount),
                    "annual_income": annual_income,
                    "reason": "requested_above_50_percent_income",
                }

        if application.term_months > 240:
            risk_score += 10
            factors["term_months"] = {
                "points": 10,
                "term_months": application.term_months,
                "reason": "term_exceeds_240_months",
            }

        factors["total_risk_score"] = risk_score
        return risk_score, factors

    @staticmethod
    def _map_risk_level(risk_score: int) -> RiskLevel:
        if risk_score >= 60:
            return RiskLevel.HIGH
        if risk_score >= 30:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    async def _notify_high_risk(self, application, assessment, actor_id: UUID) -> None:
        recipients = {actor_id}
        underwriters = await self.user_repo.get_users_by_role_name("underwriter")
        for user in underwriters:
            recipients.add(user.id)

        for user_id in recipients:
            notification = Notification(
                user_id=user_id,
                title="High Risk Loan Application",
                message=(
                    f"Application {application.application_number} was flagged as HIGH risk "
                    f"(score {assessment.risk_score}). Immediate review required."
                ),
                type="high_risk_alert",
                created_by=actor_id,
                updated_by=actor_id,
            )
            await self.notification_repo.create(notification)
