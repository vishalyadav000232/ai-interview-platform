from pydantic import BaseModel
from uuid import UUID
from datetime import datetime




class RefreshTokenCreate(BaseModel):
    user_id : UUID
    jti : str
    token_hash : str
    expires_at : datetime