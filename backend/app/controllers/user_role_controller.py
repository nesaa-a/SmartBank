from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.auth import User, UserRole
from app.repositories.user_role_repository import UserRoleRepository
from app.schemas.auth import UserRoleAssign

router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def assign_user_role(
    payload: UserRoleAssign,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = UserRoleRepository(session)
    entity = UserRole(
        user_id=payload.user_id,
        role_id=payload.role_id,
        created_by=current_user.id,
        updated_by=current_user.id,
    )
    return await repo.create(entity)


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_role(
    entity_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = UserRoleRepository(session)
    entity = await repo.get_by_id(entity_id)
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await repo.delete(entity)
