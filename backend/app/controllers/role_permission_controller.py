from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import RolePermission, User
from app.repositories.role_permission_repository import RolePermissionRepository
from app.schemas.auth import RolePermissionAssign

router = APIRouter(prefix="/role-permissions", tags=["role-permissions"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def assign_role_permission(
    payload: RolePermissionAssign,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = RolePermissionRepository(session)
    entity = RolePermission(
        role_id=payload.role_id,
        permission_id=payload.permission_id,
        created_by=current_user.id,
        updated_by=current_user.id,
    )
    return await repo.create(entity)


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_permission(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = RolePermissionRepository(session)
    entity = await repo.get_by_id(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await repo.delete(entity)
