from fastapi import Depends

from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.interface.resume import ResumeServiceInterface
from app.services.resume import ResumeService




from app.dependencies.repo_deps import get_resume_repo


def get_resume_service(
    resume_repository: ResumeRepositoryInterface = Depends(get_resume_repo),
) -> ResumeServiceInterface:
    return ResumeService(resume_repository)