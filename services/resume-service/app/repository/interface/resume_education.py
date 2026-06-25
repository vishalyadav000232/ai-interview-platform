from abc import ABC, abstractmethod
from uuid import UUID

from app.models.resume_education import ResumeEducation
from app.repository.interface.base import BaseRepositoryInterface


class ResumeEducationRepositoryInterface(
    BaseRepositoryInterface[ResumeEducation],
    ABC,
):

    @abstractmethod
    async def bulk_create(
        self,
        educations: list[ResumeEducation],
        commit: bool = True,
    ) -> list[ResumeEducation]:
        pass

    @abstractmethod
    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeEducation]:
        pass

    @abstractmethod
    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        pass