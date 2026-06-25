from abc import ABC , abstractmethod

class ResumeParserInterface(ABC):
    
    
    @abstractmethod
    async def parse(self , text : str )->dict:
        pass