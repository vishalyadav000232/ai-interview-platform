from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume_skills import ResumeSkill
from app.repository.base import BaseRepository
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface


class ResumeSkillRepository(
    BaseRepository[ResumeSkill],
    ResumeSkillRepositoryInterface,
):

    def __init__(self, db: AsyncSession,) -> None:
        super().__init__(db, ResumeSkill)

    async def bulk_create(
        self,
        skills: list[ResumeSkill],
        commit: bool = True,
    ) -> list[ResumeSkill]:
        self.db.add_all(skills)

        if commit:
            await self.db.commit()

            for skill in skills:
                await self.db.refresh(skill)

        return skills

    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeSkill]:
        result = await self.db.execute(
            select(ResumeSkill).where(
                ResumeSkill.resume_id == resume_id
            )
        )

        return list(result.scalars().all())

    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        await self.db.execute(
            delete(ResumeSkill).where(
                ResumeSkill.resume_id == resume_id
            )
        )

        if commit:
            await self.db.commit()