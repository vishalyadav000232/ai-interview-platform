import logging
from pathlib import Path
from uuid import UUID

from app.models.resume import ResumeStatus
from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.parser.interface.resume_text_extractor import ResumeTextExtractorInterface
from app.services.parser.interface.resume_parser import ResumeParserInterface


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

            text = await self.text_extractor.extract_text(file_path)

            parsed_data = await self.resume_parser.parse(text)

            # Next step:
            # save parsed_data into resume_profile, resume_skills, etc.
            
            print(parsed_data)

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

        except Exception as exc:
            logger.exception(
                "Background resume parsing failed",
                extra={
                    "resume_id": str(resume_id),
                    "file_path": str(file_path),
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason=str(exc),
            )