from abc import ABC, abstractmethod
from uuid import UUID

from app.models.resume import Resume, ResumeStatus
from app.repository.interface.base import BaseRepositoryInterface

class ResumeRepositoryInterface(
    BaseRepositoryInterface,
    ABC):

    @abstractmethod
    async def create(self, resume: Resume) -> Resume:
        pass

    @abstractmethod
    async def get_by_id(self, resume_id: UUID) -> Resume | None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Resume]:
        pass

    @abstractmethod
    async def get_active_by_user_id(self, user_id: UUID) -> list[Resume]:
        pass

    @abstractmethod
    async def update_status(
        self,
        resume_id: UUID,
        status: ResumeStatus,
        failure_reason: str | None = None
    ) -> Resume | None:
        pass

    @abstractmethod
    async def update_parsed_text(
        self,
        resume_id: UUID,
        parsed_text: str
    ) -> Resume | None:
        pass

    @abstractmethod
    async def soft_delete(self, resume_id: UUID) -> bool:
        pass