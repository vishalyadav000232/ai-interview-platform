from abc import ABC, abstractmethod
from uuid import UUID

from app.models.refresh_token import RefreshToken


class RefreshTokenServiceInterface(ABC):

    @abstractmethod
    async def create_token(
        self,
        user_id: UUID | str,
        jti: str,
        token_hash: str,
        expires_at,
    ) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def validate_token(
        self,
        jti: str,
        token_hash: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def revoke_token(
        self,
        jti: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def revoke_all_for_user(
        self,
        user_id: UUID | str,
    ) -> int:
        raise NotImplementedError