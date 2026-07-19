import logging
from pathlib import Path
from uuid import UUID

from arq.connections import RedisSettings

from app.core.config import settings
from app.database.session import AsyncLoaclSession
from app.factories.resume_processing_factory import (
    build_resume_processing_service,
)


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

    try:
        async with AsyncLoaclSession() as db:
            processing_service = build_resume_processing_service(db)

            await processing_service.process_resume(
                resume_id=UUID(resume_id),
                file_path=Path(file_path),
            )

        logger.info(
            "Resume processed successfully | resume_id=%s",
            resume_id,
        )

    except Exception:
        logger.exception(
            "Resume processing failed | resume_id=%s",
            resume_id,
        )
        raise


class WorkerSettings:
    functions = [
        process_resume_job,
    ]

    redis_settings = RedisSettings.from_dsn(
        settings.REDIS_URL
    )
