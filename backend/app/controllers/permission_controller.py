from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User
from app.schemas.auth import PermissionResponse
from app.schemas.common import PaginatedResponse
from app.services.permission_service import PermissionService
from app.schemas.auth import PermissionCreate
from app.schemas.auth import PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("", response_model=PaginatedResponse[PermissionResponse])
async def list_permission(
    skip: int = 0,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PermissionService(session)
    items = await service.list(skip=skip, limit=limit)
    total = await service.count()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=PermissionResponse)
async def get_permission(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PermissionService(session)
    entity = await service.get(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    payload: PermissionCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PermissionService(session)
    return await service.create(payload, actor_id=current_user.id)

@router.patch("/{entity_id}", response_model=PermissionResponse)
async def update_permission(
    entity_id: UUID,
    payload: PermissionUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PermissionService(session)
    entity = await service.update(entity_id, payload, actor_id=current_user.id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PermissionService(session)
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
