from abc import ABC, abstractmethod
from uuid import UUID

from app.models.user import User
from app.schemas.user import CreateUser


class UserServiceInterface(ABC):

    @abstractmethod
    async def create_user(self, user: CreateUser) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def update_user(self, user_id: UUID, data: dict) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def verify_email(self,user_id: UUID) -> User:
        pass