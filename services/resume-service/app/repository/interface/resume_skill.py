from abc import ABC, abstractmethod
from uuid import UUID

from app.models.resume_skills import ResumeSkill
from app.repository.interface.base import BaseRepositoryInterface


class ResumeSkillRepositoryInterface(
    BaseRepositoryInterface[ResumeSkill],
    ABC,
):

    @abstractmethod
    async def bulk_create(
        self,
        skills: list[ResumeSkill],
        commit: bool = True,
    ) -> list[ResumeSkill]:
        pass

    @abstractmethod
    async def get_by_resume_id(
        self,
        resume_id: UUID,
    ) -> list[ResumeSkill]:
        pass

    @abstractmethod
    async def delete_by_resume_id(
        self,
        resume_id: UUID,
        commit: bool = True,
    ) -> None:
        pass