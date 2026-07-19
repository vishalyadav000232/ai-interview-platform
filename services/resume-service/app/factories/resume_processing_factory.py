from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.resume import ResumeRepository
from app.repositories.resume_profile import ResumeProfileRepository
from app.repositories.resume_skill import ResumeSkillRepository
from app.repositories.resume_education import ResumeEducationRepository
from app.repositories.resume_experience import ResumeExperienceRepository
from app.repositories.resume_project import ResumeProjectRepository
from app.repositories.resume_analysis import ResumeAnalysisRepository

from app.services.resume_processing import ResumeProcessingService
from app.services.resume_parser import ResumeParsingService
from app.services.resume_analysis import ResumeAnalysisService

from app.services.pdf_extractor import PDFTextExtractor
from app.services.resume_text_parser import ResumeParser


def build_resume_processing_service(
    db: AsyncSession,
) -> ResumeProcessingService:
    # Repositories
    resume_repo = ResumeRepository(db)
    profile_repo = ResumeProfileRepository(db)
    skill_repo = ResumeSkillRepository(db)
    education_repo = ResumeEducationRepository(db)
    experience_repo = ResumeExperienceRepository(db)
    project_repo = ResumeProjectRepository(db)
    analysis_repo = ResumeAnalysisRepository(db)

    # Stateless helper services
    text_extractor = PDFTextExtractor()
    resume_parser = ResumeParser()

    # Parsing service
    parsing_service = ResumeParsingService(
        resume_repo=resume_repo,
        text_extractor=text_extractor,
        resume_parser=resume_parser,
        resume_profile_repo=profile_repo,
        skill_repo=skill_repo,
        edu_repo=education_repo,
        project_repo=project_repo,
        exp_repo=experience_repo,
    )

    # Analysis service
    analysis_service = ResumeAnalysisService(
        resume_repo=resume_repo,
        profile_repo=profile_repo,
        skill_repo=skill_repo,
        education_repo=education_repo,
        experience_repo=experience_repo,
        analysis_repo=analysis_repo,
        project_repo=project_repo,
    )

    return ResumeProcessingService(
        resume_repo=resume_repo,
        parsing_service=parsing_service,
        analysis_service=analysis_service,
    )
