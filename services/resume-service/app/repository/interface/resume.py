from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.models.resume import Resume, ResumeStatus


class ResumeRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Resume]:
        raise NotImplementedError

    @abstractmethod
    async def get_active_by_user_id(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Resume]:
        raise NotImplementedError

    @abstractmethod
    async def update_status(
        self,
        resume_id: UUID,
        status: ResumeStatus,
        failure_reason: str | None = None,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def mark_queued(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def mark_processing(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def mark_analyzed(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def mark_failed(
        self,
        resume_id: UUID,
        failure_reason: str,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def update_parsed_text(
        self,
        resume_id: UUID,
        parsed_text: str,
        commit: bool = True,
    ) -> Resume | None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_stale_processing_resumes(
        self,
        before: datetime,
    ) -> list[Resume]:
        raise NotImplementedError
