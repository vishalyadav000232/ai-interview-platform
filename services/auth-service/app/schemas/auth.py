from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr , ConfigDict , Field


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: UUID
    first_name: str
    last_name: str | None = None
    email: EmailStr
    is_active: bool
    is_email_verified: bool
    created_at: datetime

        
class DataReasponse(BaseModel):
    user : AuthUserResponse
    verification_link : str | None = None
   


class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: DataReasponse
    
class LoginResponse(BaseModel):
    success : bool
    message: str
    access_token : str
    token_type : str | None = None
    data : DataReasponse
    

class ChangePassword(BaseModel):
    old_password : str = Field( min_length=6 ,max_length=30)
    new_password : str = Field( min_length=6 ,max_length=30)
    

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )