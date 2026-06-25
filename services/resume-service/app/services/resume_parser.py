import logging
from pathlib import Path
from uuid import UUID

from app.core.exceptions.exception import (
    EmptyResumeTextException,
    ResumeException,
    ResumeParsedDataInvalidException,
    ResumeParsingException,
    ResumeTextExtractionException,
)
from app.models.resume import ResumeStatus
from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.parser.interface.resume_parser import ResumeParserInterface
from app.services.parser.interface.resume_text_extractor import (
    ResumeTextExtractorInterface,
)

logger = logging.getLogger(__name__)


class ResumeParsingService:
    def __init__(
        self,
        resume_repo: ResumeRepositoryInterface,
        text_extractor: ResumeTextExtractorInterface,
        resume_parser: ResumeParserInterface,
    ):
        self.resume_repo = resume_repo
        self.text_extractor = text_extractor
        self.resume_parser = resume_parser

    async def process_resume(
        self,
        resume_id: UUID,
        file_path: Path,
    ) -> None:
        logger.info(
            "Starting background resume parsing",
            extra={
                "resume_id": str(resume_id),
                "file_path": str(file_path),
            },
        )

        try:
            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.PROCESSING,
            )

            try:
                text = await self.text_extractor.extract_text(file_path)
            except Exception as exc:
                raise ResumeTextExtractionException() from exc

            if not text or not text.strip():
                raise EmptyResumeTextException()

            try:
                parsed_data = await self.resume_parser.parse(text)
            except Exception as exc:
                raise ResumeParsingException() from exc

            if not isinstance(parsed_data, dict):
                raise ResumeParsedDataInvalidException()

            await self.resume_repo.update_parsed_text(
                resume_id=resume_id,
                parsed_text=text,
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.ANALYZED,
            )

            logger.info(
                "Background resume parsing completed",
                extra={
                    "resume_id": str(resume_id),
                    "skills_count": len(parsed_data.get("skills", [])),
                },
            )

        except ResumeException as exc:
            logger.warning(
                "Resume parsing failed",
                extra={
                    "resume_id": str(resume_id),
                    "file_path": str(file_path),
                    "error_code": exc.error_code,
                    "error": exc.message,
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason=exc.message,
            )

        except Exception:
            logger.exception(
                "Unexpected resume parsing error",
                extra={
                    "resume_id": str(resume_id),
                    "file_path": str(file_path),
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason="Unexpected resume parsing error",
            )