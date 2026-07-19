import logging
from pathlib import Path
from uuid import UUID

from arq import Retry
from arq.connections import RedisSettings

from app.core.config import settings
from app.database.session import AsyncLoaclSession
from app.factories.resume_processing_factory import (
    build_resume_processing_service,
)
from app.repository.resume import ResumeRepository

logger = logging.getLogger(__name__)


async def process_resume_job(
    ctx: dict,
    resume_id: str,
    file_path: str,
) -> None:
    logger.info(
        "Resume worker received job | resume_id=%s | file_path=%s",
        resume_id,
        file_path,
    )

    async with AsyncLoaclSession() as db:
        resume_repo = ResumeRepository(db)

        try:
            await resume_repo.mark_processing(
                UUID(resume_id),
            )

            processing_service = build_resume_processing_service(db)

            await processing_service.process_resume(
                resume_id=UUID(resume_id),
                file_path=Path(file_path),
            )

            await resume_repo.mark_analyzed(
                UUID(resume_id),
            )

            logger.info(
                "Resume processed successfully | resume_id=%s",
                resume_id,
            )

        except Exception as error:
            current_try = ctx["job_try"]

            logger.exception(
                "Resume processing failed | resume_id=%s | try=%s",
                resume_id,
                current_try,
            )

            if current_try >= 3:
                await resume_repo.mark_failed(
                    UUID(resume_id),
                    failure_reason=str(error),
                )

                logger.error(
                    "Resume permanently failed | resume_id=%s",
                    resume_id,
                )

                return

            logger.warning(
                "Retrying resume processing | resume_id=%s | next_try=%s",
                resume_id,
                current_try + 1,
            )

            raise Retry(defer=5)


class WorkerSettings:
    functions = [
        process_resume_job,
    ]

    redis_settings = RedisSettings.from_dsn(
        settings.REDIS_URL,
    )

    max_tries = 3
