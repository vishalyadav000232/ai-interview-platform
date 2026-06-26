from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface
from app.repository.base import BaseRepository
from app.models.resume_exprience import ResumeExperience


class ResumeExprienceRepository(
    BaseRepository[ResumeExperience],
    ResumeExprienceRepositoryInteraface,
):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ResumeExperience)

    async def bulk_create(
        self,
        expriences: list[ResumeExperience],
        commit: bool = True,
    ) -> list[ResumeExperience]:
        try:
            self.db.add_all(expriences)

            if commit:
                await self.db.commit()

                for exp in expriences:
                    await self.db.refresh(exp)

            return expriences

        except Exception:
            await self.db.rollback()
            raise