from abc import ABC, abstractmethod
from uuid import UUID
from app.models.resume_project import ResumeProject
from app.repository.interface.base import BaseRepositoryInterface


class ResumeProjectRepositoryInterface(
    BaseRepositoryInterface[ResumeProject],
    ABC,
):

    @abstractmethod
    async def bulk_create(
        self,
        skills: list[ResumeProject],
        commit: bool = True,
    ) -> list[ResumeProject]:
        pass

    @abstractmethod
    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeProject]:
        pass

    @abstractmethod
    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        pass