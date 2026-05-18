from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.common import PaginatedResponse
from app.schemas.loan import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    LoanApplicationUpdate,
    LoanApplicationWithRiskResponse,
)
from app.services.loan_application_service import LoanApplicationService
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loan-applications", tags=["loan-applications"])


@router.get("", response_model=PaginatedResponse[LoanApplicationResponse])
async def list_loan_applications(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LoanApplicationService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{entity_id}", response_model=LoanApplicationResponse)
async def get_loan_application(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LoanApplicationService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity


@router.post("", response_model=LoanApplicationWithRiskResponse, status_code=status.HTTP_201_CREATED)
async def create_loan_application(
    payload: LoanApplicationCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LoanService(session)
    return await service.create_application(payload, actor_id=current_user.id)


@router.patch("/{entity_id}", response_model=LoanApplicationResponse)
async def update_loan_application(
    entity_id: UUID,
    payload: LoanApplicationUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LoanApplicationService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan_application(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = LoanApplicationService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
