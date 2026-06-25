from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID


class ResumeParsingServiceInterface(ABC):

    @abstractmethod
    async def process_resume(
        self,
        resume_id: UUID,
        file_path: Path,
    ) -> None:
        """
        Extract, parse and persist structured resume data.
        """
        raise NotImplementedError