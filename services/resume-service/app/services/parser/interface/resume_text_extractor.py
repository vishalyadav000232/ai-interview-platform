from abc import ABC, abstractmethod
from pathlib import Path


class ResumeTextExtractorInterface(ABC):

    @abstractmethod
    async def extract_text(self,file_path: Path,) -> str:
        pass