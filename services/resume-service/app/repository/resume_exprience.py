from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface
from app.repository.base import BaseRepository
from app.models.resume_exprience import ResumeExperience
from uuid import UUID

class ResumeExprienceRepository(
    BaseRepository[ResumeExperience],
    ResumeExprienceRepositoryInteraface,
):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ResumeExperience)

    async def bulk_create(
    self,
    experiences: list[ResumeExperience],
    commit: bool = True,
) -> list[ResumeExperience]:
        if not experiences:
            return []

        try:
            self.db.add_all(experiences)

            if commit:
                await self.db.commit()

                for exp in experiences:
                    await self.db.refresh(exp)
            else:
                await self.db.flush()

            return experiences

        except Exception:
            await self.db.rollback()
            raise
        
        
    async def get_by_resume_id(self, resume_id: UUID) -> list[ResumeExperience]:
        try:
            stmt = (
                select(ResumeExperience)
                .where(ResumeExperience.resume_id == resume_id)
                .order_by(ResumeExperience.created_at.desc())
            )

            result = await self.db.execute(stmt)

            return list(result.scalars().all())

        except Exception:
            raise