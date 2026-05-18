from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.loan import AmortizationScheduleResponse
from app.schemas.common import PaginatedResponse
from app.services.amortization_schedule_service import AmortizationScheduleService
from app.schemas.loan import AmortizationScheduleCreate
from app.schemas.loan import AmortizationScheduleUpdate

router = APIRouter(prefix="/amortization-schedules", tags=["amortization-schedules"])

@router.get("", response_model=PaginatedResponse[AmortizationScheduleResponse])
async def list_amortization_schedule(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AmortizationScheduleService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=AmortizationScheduleResponse)
async def get_amortization_schedule(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AmortizationScheduleService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=AmortizationScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_amortization_schedule(
    payload: AmortizationScheduleCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AmortizationScheduleService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=AmortizationScheduleResponse)
async def update_amortization_schedule(
    entity_id: UUID,
    payload: AmortizationScheduleUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AmortizationScheduleService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_amortization_schedule(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AmortizationScheduleService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
