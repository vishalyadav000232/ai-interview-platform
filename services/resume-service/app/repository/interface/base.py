from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepositoryInterface(ABC, Generic[ModelType]):

    @abstractmethod
    async def create(
        self,
        obj: ModelType,
        commit: bool = True,
    ) -> ModelType:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        id: UUID,
    ) -> ModelType | None:
        pass

    @abstractmethod
    async def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ModelType]:
        pass

    @abstractmethod
    async def update(
        self,
        obj: ModelType,
        data: dict[str, Any],
        commit: bool = True,
    ) -> ModelType:
        pass

    @abstractmethod
    async def delete(
        self,
        obj: ModelType,
        commit: bool = True,
    ) -> None:
        pass

    @abstractmethod
    async def save(self) -> None:
        pass

    @abstractmethod
    async def refresh(
        self,
        obj: ModelType,
    ) -> ModelType:
        pass
    @abstractmethod
    async def rollback(self )->None:
        pass