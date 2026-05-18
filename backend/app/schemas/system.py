from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import AuditResponseMixin


class AuditLogCreate(BaseModel):
    action: str
    entity_type: str
    entity_id: UUID | None = None
    ip_address: str | None = None
    details: dict | None = None


class AuditLogResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID | None
    action: str
    entity_type: str
    entity_id: UUID | None
    ip_address: str | None
    details: dict | None


class NotificationCreate(BaseModel):
    user_id: UUID
    title: str
    message: str
    type: str


class NotificationUpdate(BaseModel):
    is_read: bool | None = None


class NotificationResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    title: str
    message: str
    type: str
    is_read: bool
    read_at: datetime | None


class SettingCreate(BaseModel):
    key: str
    value: str
    category: str
    is_public: bool = False


class SettingUpdate(BaseModel):
    value: str | None = None
    category: str | None = None
    is_public: bool | None = None


class SettingResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str
    category: str
    is_public: bool


class FileCreate(BaseModel):
    filename: str
    storage_path: str
    mime_type: str
    size_bytes: int = Field(ge=0)
    entity_type: str | None = None
    entity_id: UUID | None = None


class FileResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)

    filename: str
    storage_path: str
    mime_type: str
    size_bytes: int
    entity_type: str | None
    entity_id: UUID | None
    uploaded_by: UUID | None
