from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class AuthUserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str | None = None
    email: EmailStr
    is_active: bool
    is_email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: AuthUserResponse