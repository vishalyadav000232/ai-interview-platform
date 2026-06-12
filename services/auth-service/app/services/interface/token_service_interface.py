from abc import ABC, abstractmethod


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