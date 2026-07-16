from abc import ABC , abstractmethod
from app.models.resume_analysis import ResumeAnalysis
from uuid import UUID



class ResumeAnalysisServiceInterface(ABC):



    @abstractmethod
    async def analyze_resume(
        self ,
        resume_id : UUID
    ):
        ''' analyze the resume and retrun the anlyze'''
        pass

    @abstractmethod
    async def get_resume_analysis(
    self,
    resume_id: UUID,
) -> ResumeAnalysis:
         pass
