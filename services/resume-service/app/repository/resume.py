import logging
from uuid import UUID

from sqlalchemy import select , update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume, ResumeStatus
from app.repository.interface.resume import ResumeRepositoryInterface


logger = logging.getLogger(__name__)


class ResumeRepository(ResumeRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, resume: Resume) -> Resume:
        try:
            self.db.add(resume)

            await self.db.commit()
            await self.db.refresh(resume)

            return resume

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to create resume",
                extra={
                    "user_id": str(resume.user_id),
                },
            )

            raise

    async def get_by_id(self, resume_id: UUID) -> Resume | None:
        result = await self.db.execute(
            update(Resume).where(
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
    ) -> Resume | None:
        try:
            
            values = {
                "status":status
            }
            
            if failure_reason is not None:
                values["failure_reason"]  = failure_reason
                
            result = self.db.execute(
                update(Resume).where(
                    Resume.id == resume_id
                ).values(**values)
            )
            
            if result.rowcount == 0:
                await self.db.rollback()
                return None

            await self.db.commit()
            await self.db.refresh()

            return await self.get_by_id(resume_id)

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
    ) -> Resume | None:
        try:
            resume = await self.get_by_id(resume_id)

            if resume is None:
                return None

            resume.parsed_text = parsed_text
            resume.status = ResumeStatus.ANALYZED

            await self.db.commit()
            await self.db.refresh(resume)

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

    async def soft_delete(self, resume_id: UUID) -> bool:
        try:
            resume = await self.get_by_id(resume_id)

            if resume is None:
                return False

            resume.is_active = False
            resume.is_deleted = True

            await self.db.commit()

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