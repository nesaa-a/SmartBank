from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.loan import RiskMitigationRuleResponse
from app.schemas.common import PaginatedResponse
from app.services.risk_mitigation_rule_service import RiskMitigationRuleService
from app.schemas.loan import RiskMitigationRuleCreate
from app.schemas.loan import RiskMitigationRuleUpdate

router = APIRouter(prefix="/risk-mitigation-rules", tags=["risk-mitigation-rules"])

@router.get("", response_model=PaginatedResponse[RiskMitigationRuleResponse])
async def list_risk_mitigation_rule(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskMitigationRuleService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=RiskMitigationRuleResponse)
async def get_risk_mitigation_rule(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskMitigationRuleService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=RiskMitigationRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_mitigation_rule(
    payload: RiskMitigationRuleCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskMitigationRuleService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=RiskMitigationRuleResponse)
async def update_risk_mitigation_rule(
    entity_id: UUID,
    payload: RiskMitigationRuleUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskMitigationRuleService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_risk_mitigation_rule(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = RiskMitigationRuleService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
