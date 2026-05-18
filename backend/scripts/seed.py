"""Seed default roles, permissions, and an admin user."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.auth import Permission, Role, RolePermission, User, UserRole
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository

ROLES = [
    ("admin", "System administrator with full access"),
    ("underwriter", "Reviews and approves loan applications"),
    ("analyst", "Analyzes risk and customer financial data"),
]

PERMISSIONS = [
    ("user:read", "users", "read", "Read users"),
    ("user:write", "users", "write", "Create and update users"),
    ("loan:create", "loans", "create", "Create loan applications"),
    ("loan:read", "loans", "read", "Read loan data"),
    ("loan:approve", "loans", "approve", "Approve loans"),
    ("risk:read", "risk", "read", "Read risk assessments"),
    ("risk:write", "risk", "write", "Manage risk rules"),
]

ADMIN_EMAIL = "admin@bank.local"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin123!ChangeMe"


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        role_repo = RoleRepository(session)
        perm_repo = PermissionRepository(session)
        user_repo = UserRepository(session)

        role_map: dict[str, Role] = {}
        for name, description in ROLES:
            role = await role_repo.get_by_name(name)
            if role is None:
                role = Role(name=name, description=description)
                role = await role_repo.create(role)
            role_map[name] = role

        perm_map: dict[str, Permission] = {}
        for code, resource, action, description in PERMISSIONS:
            permission = await perm_repo.get_by_code(code)
            if permission is None:
                permission = Permission(
                    code=code,
                    resource=resource,
                    action=action,
                    description=description,
                )
                permission = await perm_repo.create(permission)
            perm_map[code] = permission

        admin_role = role_map["admin"]
        for permission in perm_map.values():
            stmt = select(RolePermission).where(
                RolePermission.role_id == admin_role.id,
                RolePermission.permission_id == permission.id,
            )
            result = await session.execute(stmt)
            if result.scalar_one_or_none() is None:
                session.add(
                    RolePermission(
                        role_id=admin_role.id,
                        permission_id=permission.id,
                    )
                )

        admin_user = await user_repo.get_by_email(ADMIN_EMAIL)
        if admin_user is None:
            admin_user = User(
                email=ADMIN_EMAIL,
                username=ADMIN_USERNAME,
                full_name="System Administrator",
                hashed_password=get_password_hash(ADMIN_PASSWORD),
                is_active=True,
                is_superuser=True,
            )
            admin_user = await user_repo.create(admin_user)
            session.add(
                UserRole(
                    user_id=admin_user.id,
                    role_id=admin_role.id,
                    created_by=admin_user.id,
                    updated_by=admin_user.id,
                )
            )

        await session.commit()
        print("Seed completed.")
        print(f"Admin login: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
