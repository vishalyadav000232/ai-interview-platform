from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface


from app.repository.resume import ResumeRepository
from app.repository.resume_profile import ResumeProfileRepository
from app.repository.resume_skills import ResumeSkillRepository
from app.repository.resume_education import ResumeEducationRepository
from app.repository.resume_project import ResumeProjectRepository
from app.repository.resume_exprience import ResumeExprienceRepository

async def get_resume_repo(
    db: AsyncSession = Depends(get_db),
) -> ResumeRepositoryInterface:
    return ResumeRepository(db)


async def get_resume_profile_repository(
    db: AsyncSession = Depends(get_db),
) -> ResumeProfileRepositoryInterface:
    return ResumeProfileRepository(db)


async def get_resume_skill_repository(
    db: AsyncSession = Depends(get_db),
) -> ResumeSkillRepositoryInterface:
    return ResumeSkillRepository(db)


async def get_resume_education_repository(
    db: AsyncSession = Depends(get_db),
) -> ResumeEducationRepositoryInterface:
    return ResumeEducationRepository(db)


async def get_resume_project_repository(
    db : AsyncSession = Depends(get_db)
)->ResumeProjectRepositoryInterface:
    return  ResumeProjectRepository(db)

async def get_resume_exp_repository(
    db : AsyncSession = Depends(get_db),
)-> ResumeExprienceRepositoryInteraface:
    return ResumeExprienceRepository(db)