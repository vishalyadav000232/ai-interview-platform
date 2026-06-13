

from pydantic import BaseModel , EmailStr
from uuid import UUID



class CreateUser(BaseModel):
    id : UUID
    first_name : str
    email : EmailStr
    password_hash : str
    
    
    