from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import UploadFile

from app.models.resume import Resume


class ResumeServiceInterface(ABC):

    @abstractmethod
    async def upload_resume(
        self,
        user_id: UUID,
        file: UploadFile,
    ) -> Resume:
        pass

    @abstractmethod
    async def get_resume(
        self,
        user_id : UUID,
        resume_id: UUID,
    ) -> Resume | None:
        pass

    @abstractmethod
    async def get_user_resumes(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        pass

    @abstractmethod
    async def delete_resume(
        self,
        resume_id: UUID,
    ) -> bool:
        pass
    @abstractmethod
    async def mark_resume_queued(
        self,
        resume_id: UUID,
    ):
        raise NotImplementedError
