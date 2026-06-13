
from datetime import datetime
from pydantic import BaseModel , EmailStr , Field
from uuid import UUID



class CreateUser(BaseModel):
    
    first_name : str = Field(...,min_length=2 , max_length=50)
    last_name : str | None = Field(default=None , max_length=50)
    email : EmailStr
    password : str = Field(... ,min_length=4 , max_length=128 )
    

class UpdateUser(BaseModel):
    first_name : str | None = Field(default=None , min_length=2 , max_length=50)
    last_name : str | None = Field(default=None , min_length=2 , max_length=50)
    
    
class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str | None = None
    email: EmailStr
    role: str | None = None
    is_active: bool
    is_email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True