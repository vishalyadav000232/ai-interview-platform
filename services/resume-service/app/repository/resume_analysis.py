import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume_analysis import ResumeAnalysis
from app.repository.base import BaseRepository
from app.repository.interface.resume_analysis import (
    ResumeAnalysisRepositoryInterface,
)

logger = logging.getLogger(__name__)


class ResumeAnalysisRepository(
    BaseRepository[ResumeAnalysis],
    ResumeAnalysisRepositoryInterface,
):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ResumeAnalysis)

    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeAnalysis] | None:
        try:
            stmt = (
                select(ResumeAnalysis)
                .where(ResumeAnalysis.resume_id == resume_id).
                order_by(ResumeAnalysis.created_at.desc())
            )

            result = await self.db.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.exception(
                "Failed to fetch resume analysis for resume_id=%s",
                resume_id,
            )
            raise
    async def get_latest_by_resume_id(
        self,
        resume_id: UUID,
    ) -> ResumeAnalysis | None:
        try:
            stmt = (
                select(ResumeAnalysis)
                .where(ResumeAnalysis.resume_id == resume_id)
                .order_by(ResumeAnalysis.created_at.desc())
                .limit(1)
            )

            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        
        except Exception as e:
            logger.exception(
                "Failed to fetch resume analysis for resume_id=%s",
                resume_id
            )