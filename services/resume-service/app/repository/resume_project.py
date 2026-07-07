from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.resume_project import ResumeProject
from app.repository.base import BaseRepository
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface


class ResumeProjectRepository(
    BaseRepository[ResumeProject],
    ResumeProjectRepositoryInterface,
):

    def __init__(self, db: AsyncSession,) -> None:
        super().__init__(db, ResumeProject)

    async def bulk_create(
        self,
        projects: list[ResumeProject],
        commit: bool = True,
    ) -> list[ResumeProject]:
        self.db.add_all(projects)

        if commit:
            await self.db.commit()

            for skill in projects:
                await self.db.refresh(skill)
        else:
            await self.db.flush()

        return projects

    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeProject]:
        result = await self.db.execute(
            select(ResumeProject).where(
                ResumeProject.resume_id == resume_id
            )
        )

        return list(result.scalars().all())

    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        await self.db.execute(
            delete(ResumeProject).where(
                ResumeProject.resume_id == resume_id
            )
        )

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()