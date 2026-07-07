from abc import ABC, abstractmethod
from uuid import UUID

from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshTokenCreate


class RefreshTokenRepositoryInterface(ABC):

    @abstractmethod
    async def create(
        self,
        payload: RefreshTokenCreate,
    ) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        raise NotImplementedError

    @abstractmethod
    async def revoke(
        self,
        token_id: UUID,
    ) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def revoke_all_for_user(
        self,
        user_id: UUID,
    ) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_jti(self , jti: str)->RefreshToken | None:
        raise NotImplementedError