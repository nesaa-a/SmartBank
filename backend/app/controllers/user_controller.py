from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.auth import UserResponse
from app.schemas.common import PaginatedResponse
from app.services.user_service import UserService
from app.schemas.auth import UserCreate
from app.schemas.auth import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_user(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=UserResponse)
async def get_user(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=UserResponse)
async def update_user(
    entity_id: UUID,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
