from abc import ABC , abstractmethod

from uuid import UUID



class ResumeAnalysisServiceInterface(ABC):
    
    
    
    @abstractmethod
    async def analyze_resume(
        self , 
        resume_id : UUID   
    ):
        ''' analyze the resume and retrun the anlyze'''
        pass