from fastapi import Depends

from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface

from app.dependencies.repo_deps import (
    get_resume_repo,
    get_resume_profile_repository,
    get_resume_skill_repository,
    get_resume_education_repository,
)

from app.services.interface.resume import ResumeServiceInterface
from app.services.resume import ResumeService


def get_resume_service(
    resume_repo: ResumeRepositoryInterface = Depends(get_resume_repo),
    profile_repo: ResumeProfileRepositoryInterface = Depends(get_resume_profile_repository),
    skill_repo: ResumeSkillRepositoryInterface = Depends(get_resume_skill_repository),
    education_repo: ResumeEducationRepositoryInterface = Depends(get_resume_education_repository),
) -> ResumeServiceInterface:
    return ResumeService(
        resume_repo=resume_repo,
        profile_repo=profile_repo,
        skill_repo=skill_repo,
        education_repo=education_repo,
    )