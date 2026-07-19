from arq.connections import RedisSettings
from app.workers.resume_worker import process_resume_job
from app.core.config import settings
class WorkerSettings:
    functions = [
        process_resume_job,
    ]

    redis_settings = RedisSettings.from_dsn(
        settings.REDIS_URL,
    )

    max_tries = 3
