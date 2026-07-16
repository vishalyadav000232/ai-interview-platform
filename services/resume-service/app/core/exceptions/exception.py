
from fastapi import status
class ResumeException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)





class ResumeTextExtractionException(ResumeException):
    def __init__(self):
        super().__init__(
            message="Failed to extract text from resume",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="RESUME_TEXT_EXTRACTION_FAILED",
        )


class EmptyResumeTextException(ResumeException):
    def __init__(self):
        super().__init__(
            message="Extracted resume text is empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="RESUME_TEXT_EMPTY",
        )


class ResumeParsingException(ResumeException):
    def __init__(self):
        super().__init__(
            message="Failed to parse resume text",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="RESUME_PARSE_FAILED",
        )

class ResumeParsedDataInvalidException(ResumeException):
    def __init__(self):
        super().__init__(
            message="Failed to parse resume text",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESUME_PARSE_FAILED",
        )

class ResumeNotFound(ResumeException):
    def __init__(self):
        super().__init__(
            message="Resume Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESUME_NOT_FOUND",
        )
class ResumeAnalysisNotFound(ResumeException):
    def __init__(self):
        super().__init__(
            message="Resume analysis not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESUME_ANALYSIS_NOT_FOUND",
        )
