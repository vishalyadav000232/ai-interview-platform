from fastapi import Depends

from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_analysis import ResumeAnalysisRepositoryInterface
from app.repository.interface.resume_expriennc import (
    ResumeExprienceRepositoryInteraface,
)
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface

from app.dependencies.repo_deps import (
    get_resume_repo,
    get_resume_profile_repository,
    get_resume_skill_repository,
    get_resume_education_repository,
    get_resume_analysis_repo,
    get_resume_exp_repository,
    get_resume_project_repository,
)

from app.services.interface.resume import ResumeServiceInterface
from app.services.resume import ResumeService

from app.services.resume_analysis.interface.analysis import (
    ResumeAnalysisServiceInterface,
)
from app.services.resume_analysis.services.analysis import ResumeAnalysisService


def get_resume_service(
    resume_repo: ResumeRepositoryInterface = Depends(get_resume_repo),
    profile_repo: ResumeProfileRepositoryInterface = Depends(
        get_resume_profile_repository
    ),
    skill_repo: ResumeSkillRepositoryInterface = Depends(
        get_resume_skill_repository
    ),
    education_repo: ResumeEducationRepositoryInterface = Depends(
        get_resume_education_repository
    ),
) -> ResumeServiceInterface:
    return ResumeService(
        resume_repo=resume_repo,
        profile_repo=profile_repo,
        skill_repo=skill_repo,
        education_repo=education_repo,
    )


def get_resume_analysis_service(
    resume_repo: ResumeRepositoryInterface = Depends(get_resume_repo),
    profile_repo: ResumeProfileRepositoryInterface = Depends(
        get_resume_profile_repository
    ),
    skill_repo: ResumeSkillRepositoryInterface = Depends(
        get_resume_skill_repository
    ),
    education_repo: ResumeEducationRepositoryInterface = Depends(
        get_resume_education_repository
    ),
    experience_repo: ResumeExprienceRepositoryInteraface = Depends(
        get_resume_exp_repository
    ),
    analysis_repo: ResumeAnalysisRepositoryInterface = Depends(
        get_resume_analysis_repo
    ),
    project_repo : ResumeProjectRepositoryInterface = Depends(get_resume_project_repository),
) -> ResumeAnalysisServiceInterface:
    return ResumeAnalysisService(
        resume_repo=resume_repo,
        profile_repo=profile_repo,
        skill_repo=skill_repo,
        education_repo=education_repo,
        experience_repo=experience_repo,
        analysis_repo=analysis_repo,
        project_repo=project_repo
    )