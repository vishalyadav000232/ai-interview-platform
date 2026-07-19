import logging
from arq.connections import ArqRedis
from uuid import UUID
from pathlib import Path
from app.core.redis import get_redis_client


logger = logging.getLogger(__name__)

class ResumeQueue:
    def __init__(self , redis :ArqRedis ):
        self.redis = redis


    async def enqueue_resume_processing(self , resume_id : UUID , file_path : Path)->str:
        job  = await self.redis.enqueue_job(
            'process_resume_job',
            str(resume_id),
            str(file_path)
        )

        if job in None:
             raise RuntimeError(
                f"Failed to enqueue resume processing job: {resume_id}"
            )

        logger.info(
            "Resume processing job queued",
            extra={
                "resume_id": str(resume_id),
                "job_id": job.job_id,
            },
        )

        return job.job_id

def get_resume_queue() -> ResumeQueue:
    redis = get_redis_client()
    return ResumeQueue(redis=redis)








