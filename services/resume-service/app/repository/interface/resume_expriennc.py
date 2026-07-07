from abc import ABC , abstractmethod

from app.models.resume_exprience import ResumeExperience
from app.repository.interface.base import BaseRepositoryInterface
from uuid import UUID



class ResumeExprienceRepositoryInteraface(
    BaseRepositoryInterface,
    ABC):
    
    
   
    @abstractmethod
    async def bulk_create(
        self,
        exprience: list[ResumeExperience],
        commit: bool = True,
    ) -> list[ResumeExperience]:
        pass
    
    async def get_by_resume_id(self , resume_id : UUID)->ResumeExperience:
        pass