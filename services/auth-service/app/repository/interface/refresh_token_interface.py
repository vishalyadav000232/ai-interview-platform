from abc import ABC , abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshTokenCreate
from uuid import UUID



class RefreshTokenRepositoryInterface(ABC):
    
    
    @abstractmethod
    async def create(self , payload : RefreshTokenCreate , db : AsyncSession)-> RefreshToken:
        pass
    
    @abstractmethod
    async def get_by_token_hash(self , token_hash : str , db : AsyncSession)->RefreshToken:
        pass
    
    @abstractmethod
    async def revoke(self , token_id : UUID , db : AsyncSession)-> RefreshToken:
        pass
    
    @abstractmethod
    async def revoke_all_for_user( self , user_id : UUID , db : AsyncSession)-> int:
        pass