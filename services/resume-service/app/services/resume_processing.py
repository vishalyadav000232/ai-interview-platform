import logging
from pathlib import Path
from uuid import UUID

from app.models.resume import ResumeStatus
from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.interface.resume_parser import (
    ResumeParsingServiceInterface,
)
from app.services.resume_analysis.interface.analysis import (
    ResumeAnalysisServiceInterface,
)


logger = logging.getLogger(__name__)


class ResumeProcessingService:
    def __init__(
        self,
        resume_repo: ResumeRepositoryInterface,
        parsing_service: ResumeParsingServiceInterface,
        analysis_service: ResumeAnalysisServiceInterface,
    ) -> None:
        self.resume_repo = resume_repo
        self.parsing_service = parsing_service
        self.analysis_service = analysis_service

    async def process_resume(
    self,
    resume_id: UUID,
    file_path: Path,
) -> None:
        try:
            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.PROCESSING,
            )

            await self.parsing_service.process_resume(
                resume_id=resume_id,
                file_path=file_path,
            )

            await self.analysis_service.analyze_resume(
                resume_id=resume_id,
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.ANALYZED,
            )

        except Exception as exc:
            logger.exception(
                "Resume processing failed",
                extra={
                    "resume_id": str(resume_id),
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason=str(exc),
            )
