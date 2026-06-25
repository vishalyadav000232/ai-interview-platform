from abc import ABC, abstractmethod
from uuid import UUID

from app.models.resume_profile import ResumeProfile
from app.repository.interface.base import BaseRepositoryInterface


class ResumeProfileRepositoryInterface(
    BaseRepositoryInterface[ResumeProfile],
    ABC,
):

    @abstractmethod
    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> ResumeProfile | None:
        pass