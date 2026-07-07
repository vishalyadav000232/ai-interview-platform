from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume_profile import ResumeProfile
from app.repository.base import BaseRepository
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface


class ResumeProfileRepository(
    BaseRepository[ResumeProfile],
    ResumeProfileRepositoryInterface,
):

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, ResumeProfile)

    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> ResumeProfile | None:
        result = await self.db.execute(
            select(ResumeProfile).where(
                ResumeProfile.resume_id == resume_id
            )
        )

        return result.scalar_one_or_none()