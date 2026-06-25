from fastapi import Depends

from app.dependencies.repo_deps import get_resume_repo
from app.repository.interface.resume import ResumeRepositoryInterface

from app.services.interface.resume_parser import ResumeParsingServiceInterface
from app.services.resume_parser import ResumeParsingService

from app.services.parser.interface.resume_text_extractor import (
    ResumeTextExtractorInterface,
)
from app.services.parser.extractor.pdf_text_extractor import PDFTextExtractor

from app.services.parser.interface.resume_parser import ResumeParserInterface
from app.services.parser.parsers.regex_resume_pareser import RegexResumeParser


async def get_pdf_extractor_service() -> ResumeTextExtractorInterface:
    return PDFTextExtractor()


async def get_resume_parser() -> ResumeParserInterface:
    return RegexResumeParser()


async def get_resume_parse_service(
    resume_repo: ResumeRepositoryInterface = Depends(get_resume_repo),
    text_extractor: ResumeTextExtractorInterface = Depends(get_pdf_extractor_service),
    resume_parser: ResumeParserInterface = Depends(get_resume_parser),
) -> ResumeParsingServiceInterface:
    return ResumeParsingService(
        resume_repo=resume_repo,
        text_extractor=text_extractor,
        resume_parser=resume_parser,
    )