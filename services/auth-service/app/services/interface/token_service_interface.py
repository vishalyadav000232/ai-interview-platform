from abc import ABC, abstractmethod
from uuid import UUID

class TokenServiceInterface(ABC):

    @abstractmethod
    async def create_access_token(self,user_id: str,) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(self,user_id: str,) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_access_token(self,token: str,) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def verify_refresh_token( self,token: str,) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def revoke_refresh_token(self,jti: str,) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def rotate_refresh_token(self, refresh_token: str) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def revoke_all_user_sessions(self, user_id: UUID | str) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def create_email_verification_token(self, user_id : UUID |str)-> str:
        raise NotImplementedError
    @abstractmethod
    async def verify_email_verification_token(self , token : str)-> dict:
        raise NotImplementedError
    
        