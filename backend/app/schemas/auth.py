from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.common import AuditResponseMixin


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    full_name: str = Field(min_length=1, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=100)
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserResponse(UserBase, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class RoleResponse(RoleBase, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class PermissionBase(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    resource: str = Field(min_length=1, max_length=100)
    action: str = Field(min_length=1, max_length=50)
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=100)
    resource: str | None = Field(default=None, min_length=1, max_length=100)
    action: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None


class PermissionResponse(PermissionBase, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class UserRoleAssign(BaseModel):
    user_id: UUID
    role_id: UUID


class RolePermissionAssign(BaseModel):
    role_id: UUID
    permission_id: UUID


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    pass


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str
