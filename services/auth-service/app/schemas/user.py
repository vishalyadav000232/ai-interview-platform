from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class CreateUser(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UpdateUser(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str | None = None
    email: EmailStr
    role: UserRole
    is_active: bool
    is_email_verified: bool
    created_at: datetime