from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.common import PaginatedResponse
from app.schemas.loan import RiskAssessmentResponse
from app.services.risk_assessment_service import RiskAssessmentService

router = APIRouter(prefix="/risk-assessments", tags=["risk-assessments"])


@router.get("", response_model=PaginatedResponse[RiskAssessmentResponse])
async def list_risk_assessments(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskAssessmentService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{entity_id}", response_model=RiskAssessmentResponse)
async def get_risk_assessment(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskAssessmentService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity
