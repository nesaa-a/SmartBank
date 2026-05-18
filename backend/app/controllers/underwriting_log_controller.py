from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.loan import UnderwritingLogResponse
from app.schemas.common import PaginatedResponse
from app.services.underwriting_log_service import UnderwritingLogService
from app.schemas.loan import UnderwritingLogCreate
from app.schemas.loan import UnderwritingLogUpdate

router = APIRouter(prefix="/underwriting-logs", tags=["underwriting-logs"])

@router.get("", response_model=PaginatedResponse[UnderwritingLogResponse])
async def list_underwriting_log(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UnderwritingLogService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=UnderwritingLogResponse)
async def get_underwriting_log(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UnderwritingLogService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=UnderwritingLogResponse, status_code=status.HTTP_201_CREATED)
async def create_underwriting_log(
    payload: UnderwritingLogCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UnderwritingLogService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=UnderwritingLogResponse)
async def update_underwriting_log(
    entity_id: UUID,
    payload: UnderwritingLogUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UnderwritingLogService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_underwriting_log(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UnderwritingLogService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
