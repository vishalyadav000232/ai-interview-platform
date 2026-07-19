from pathlib import Path
from uuid import UUID

from arq.connections import RedisSettings

from app.core.config import settings
from app.database.session import AsyncLoaclSession
from app.factories.resume_processing_factory import (
    build_resume_processing_service,
)


async def process_resume_job(
    ctx: dict,
    resume_id: str,
    file_path: str,
) -> None:
    async with AsyncLoaclSession() as db:
        processing_service = build_resume_processing_service(db)

        await processing_service.process_resume(
            resume_id=UUID(resume_id),
            file_path=Path(file_path),
        )


class WorkerSettings:
    functions = [
        process_resume_job,
    ]

    redis_settings = RedisSettings.from_dsn(
        settings.REDIS_URL
    )
