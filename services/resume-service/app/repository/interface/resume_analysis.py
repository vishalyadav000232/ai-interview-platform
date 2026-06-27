from abc import ABC , abstractmethod

from app.repository.interface.base import BaseRepositoryInterface
from uuid import UUID
from app.models.resume_analysis import ResumeAnalysis

class ResumeAnalysisRepositoryInterface(
    BaseRepositoryInterface,
    ABC
):
    
    
    @abstractmethod
    async def get_by_resume_id(self, resume_id : UUID)-> list[ResumeAnalysis]:
        pass
      