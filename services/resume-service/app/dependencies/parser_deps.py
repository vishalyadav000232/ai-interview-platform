from fastapi import Depends

from app.dependencies.repo_deps import get_resume_repo , get_resume_profile_repository , get_resume_skill_repository , get_resume_education_repository , get_resume_project_repository , get_resume_exp_repository

from app.repository.interface.resume import ResumeRepositoryInterface

from app.services.interface.resume_parser import ResumeParsingServiceInterface
from app.services.resume_parser import ResumeParsingService

from app.services.parser.interface.resume_text_extractor import (
    ResumeTextExtractorInterface,
)
from app.services.parser.extractor.pdf_text_extractor import PDFTextExtractor

from app.services.parser.interface.resume_parser import ResumeParserInterface
from app.services.parser.parsers.regex_resume_pareser import RegexResumeParser
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface

from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface



async def get_pdf_extractor_service() -> ResumeTextExtractorInterface:
    return PDFTextExtractor()


async def get_resume_parser() -> ResumeParserInterface:
    return RegexResumeParser()


async def get_resume_parse_service(
    resume_repo: ResumeRepositoryInterface = Depends(get_resume_repo),
    text_extractor: ResumeTextExtractorInterface = Depends(get_pdf_extractor_service),
    resume_parser: ResumeParserInterface = Depends(get_resume_parser),
    resume_profile : ResumeProfileRepositoryInterface = Depends(get_resume_profile_repository),
    skill_repo : ResumeSkillRepositoryInterface = Depends(get_resume_skill_repository),
    edu_repo : ResumeEducationRepositoryInterface = Depends(get_resume_education_repository),
    project_repo : ResumeProjectRepositoryInterface = Depends(get_resume_project_repository),
    exp_repo : ResumeExprienceRepositoryInteraface = Depends(get_resume_exp_repository)
) -> ResumeParsingServiceInterface:
    return ResumeParsingService(
        resume_repo=resume_repo,
        text_extractor=text_extractor,
        resume_parser=resume_parser,
        resume_profile_repo=resume_profile,
        skill_repo=skill_repo,
        edu_repo=edu_repo,
        project_repo=project_repo,
        exp_repo=exp_repo
    )