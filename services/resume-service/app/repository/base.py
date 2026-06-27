import logging
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.repository.interface.base import BaseRepositoryInterface


logger = logging.getLogger(__name__)



ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(BaseRepositoryInterface[ModelType], Generic[ModelType]):

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType],
    ) -> None:
        self.db = db
        self.model = model

    async def create(
        self,
        obj: ModelType,
        commit: bool = True,
    ) -> ModelType:
        try:
            self.db.add(obj)

            if commit:
                await self.db.commit()
                await self.db.refresh(obj)
            else:
                await self.db.flush()

            return obj

        except Exception:
            await self.db.rollback()
            logger.exception(
                "Failed to create %s",
                self.model.__name__,
            )
            raise

    async def get_by_id(
        self,
        id: UUID,
    ) -> ModelType | None:
        try:
            result = await self.db.execute(
                select(self.model).where(self.model.id == id)
            )
            return result.scalar_one_or_none()

        except Exception:
            logger.exception(
                "Failed to fetch %s by id=%s",
                self.model.__name__,
                id,
            )
            raise

    async def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ModelType]:
        try:
            result = await self.db.execute(
                select(self.model)
                .limit(limit)
                .offset(offset)
            )

            return list(result.scalars().all())

        except Exception:
            logger.exception(
                "Failed to list %s records",
                self.model.__name__,
            )
            raise

    async def update(
        self,
        obj: ModelType,
        data: dict[str, Any],
        commit: bool = True,
    ) -> ModelType:
        try:
            for key, value in data.items():
                setattr(obj, key, value)

            if commit:
                await self.db.commit()
                await self.db.refresh(obj)
            else:
                await self.db.flush()

            return obj

        except Exception:
            await self.db.rollback()
            logger.exception(
                "Failed to update %s",
                self.model.__name__,
            )
            raise

    async def delete(
        self,
        obj: ModelType,
        commit: bool = True,
    ) -> None:
        try:
            await self.db.delete(obj)

            if commit:
                await self.db.commit()
            else:
                await self.db.flush()

        except Exception:
            await self.db.rollback()
            logger.exception(
                "Failed to delete %s",
                self.model.__name__,
            )
            raise

    async def save(self) -> None:
        try:
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            logger.exception("Failed to commit database transaction")
            raise

    async def refresh(
        self,
        obj: ModelType,
    ) -> ModelType:
        try:
            await self.db.refresh(obj)
            return obj

        except Exception:
            logger.exception(
                "Failed to refresh %s",
                self.model.__name__,
            )
            raise
    
    async def rollback(self):
        try:
            self.db.rollback()
        except Exception:
            logger.exception("Failed to rollback data trancsaction ")
            raise
    
    async def commit(self)->None:
        try:
            self.db.commit()
        except Exception:
            logger.exception(
                "Failed to rollback database transaction"
            )
        