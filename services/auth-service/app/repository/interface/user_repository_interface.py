from abc import ABC, abstractmethod

from uuid import UUID

from app.models.user import User
from app.schemas.user import CreateUser


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, user: CreateUser) -> User:
        pass

    @abstractmethod
    async def get_by_id(self,user_id: UUID) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self,email: str) -> User | None:
        pass

    @abstractmethod
    async def update(self,user: User) -> User:
        pass

    @abstractmethod
    async def delete(self,user_id: UUID) -> bool:
        pass