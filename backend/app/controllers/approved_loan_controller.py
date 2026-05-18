from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.loan import ApprovedLoanResponse
from app.schemas.common import PaginatedResponse
from app.services.approved_loan_service import ApprovedLoanService
from app.schemas.loan import ApprovedLoanCreate
from app.schemas.loan import ApprovedLoanUpdate

router = APIRouter(prefix="/approved-loans", tags=["approved-loans"])

@router.get("", response_model=PaginatedResponse[ApprovedLoanResponse])
async def list_approved_loan(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ApprovedLoanService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=ApprovedLoanResponse)
async def get_approved_loan(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ApprovedLoanService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=ApprovedLoanResponse, status_code=status.HTTP_201_CREATED)
async def create_approved_loan(
    payload: ApprovedLoanCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ApprovedLoanService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=ApprovedLoanResponse)
async def update_approved_loan(
    entity_id: UUID,
    payload: ApprovedLoanUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ApprovedLoanService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approved_loan(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ApprovedLoanService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
