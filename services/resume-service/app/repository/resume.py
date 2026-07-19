import logging
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume, ResumeStatus
from app.repository.base import BaseRepository
from app.repository.interface.resume import ResumeRepositoryInterface
from datetime import datetime

logger = logging.getLogger(__name__)


class ResumeRepository(
    BaseRepository[Resume],
    ResumeRepositoryInterface,
):
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, Resume)

    async def get_by_id(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        result = await self.db.execute(
            select(Resume).where(
                Resume.id == resume_id,
                Resume.is_deleted.is_(False),
            )
        )

        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Resume]:
        result = await self.db.execute(
            select(Resume)
            .where(
                Resume.user_id == user_id,
                Resume.is_deleted.is_(False),
            )
            .order_by(Resume.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())

    async def get_active_by_user_id(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Resume]:
        result = await self.db.execute(
            select(Resume)
            .where(
                Resume.user_id == user_id,
                Resume.is_active.is_(True),
                Resume.is_deleted.is_(False),
            )
            .order_by(Resume.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())

    async def update_status(
        self,
        resume_id: UUID,
        status: ResumeStatus,
        failure_reason: str | None = None,
        commit: bool = True,
    ) -> Resume | None:
        try:
            values = {
                "status": status,
            }

            if failure_reason is not None:
                values["failure_reason"] = failure_reason

            if status == ResumeStatus.PROCESSING:
                values["processing_started_at"] = func.now()

            if status in (ResumeStatus.ANALYZED, ResumeStatus.FAILED):
                values["processing_completed_at"] = func.now()

            result = await self.db.execute(
                update(Resume)
                .where(
                    Resume.id == resume_id,
                    Resume.is_deleted.is_(False),
                )
                .values(**values)
                .returning(Resume)
            )

            resume = result.scalar_one_or_none()

            if resume is None:
                if commit:
                    await self.db.rollback()
                return None

            if commit:
                await self.db.commit()
                await self.db.refresh(resume)
            else:
                await self.db.flush()

            return resume

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to update resume status",
                extra={
                    "resume_id": str(resume_id),
                    "status": status.value,
                },
            )

            raise

    async def update_parsed_text(
        self,
        resume_id: UUID,
        parsed_text: str,
        commit: bool = True,
    ) -> Resume | None:
        try:
            result = await self.db.execute(
                update(Resume)
                .where(
                    Resume.id == resume_id,
                    Resume.is_deleted.is_(False),
                )
                .values(
                    parsed_text=parsed_text,
                )
                .returning(Resume)
            )

            resume = result.scalar_one_or_none()

            if resume is None:
                if commit:
                    await self.db.rollback()
                return None

            if commit:
                await self.db.commit()
                await self.db.refresh(resume)
            else:
                await self.db.flush()

            return resume

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to update parsed resume text",
                extra={
                    "resume_id": str(resume_id),
                },
            )

            raise

    async def soft_delete(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> bool:
        try:
            result = await self.db.execute(
                update(Resume)
                .where(
                    Resume.id == resume_id,
                    Resume.is_deleted.is_(False),
                )
                .values(
                    is_active=False,
                    is_deleted=True,
                )
            )

            if result.rowcount == 0:
                if commit:
                    await self.db.rollback()
                return False

            if commit:
                await self.db.commit()
            else:
                await self.db.flush()

            return True

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to soft delete resume",
                extra={
                    "resume_id": str(resume_id),
                },
            )

            raise


    async def get_stale_processing_resumes(
    self,
    before: datetime,
) -> list[Resume]:
        stmt = (
            select(Resume)
            .where(
                Resume.status == ResumeStatus.PROCESSING,
                Resume.processing_started_at < before,
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
