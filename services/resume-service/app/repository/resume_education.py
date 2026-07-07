from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume_education import ResumeEducation
from app.repository.base import BaseRepository
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface


class ResumeEducationRepository(
    BaseRepository[ResumeEducation],
    ResumeEducationRepositoryInterface,
):

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, ResumeEducation)

    async def bulk_create(
        self,
        educations: list[ResumeEducation],
        commit: bool = True,
    ) -> list[ResumeEducation]:
        try:
            self.db.add_all(educations)

            if commit:
                await self.db.commit()
            

                for education in educations:
                    await self.db.refresh(education)
                    
            else:
                await self.db.flush()
                
                

            return educations
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeEducation]:
        result = await self.db.execute(
            select(ResumeEducation).where(
                ResumeEducation.resume_id == resume_id
            )
        )

        return list(result.scalars().all())

    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        try:
            await self.db.execute(
                delete(ResumeEducation).where(
                    ResumeEducation.resume_id == resume_id
                )
            )

            if commit:
                await self.db.commit()
            else:
                await self.db.flush()
                
        except Exception:
            await self.db.rollback()
            raise
                