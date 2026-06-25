import logging
from pathlib import Path

import fitz
from fastapi import status

from app.core.exceptions.error_code import ResumeErrorCode
from app.core.exceptions.exception import ResumeException
from app.services.parser.interface.resume_text_extractor import (
    ResumeTextExtractorInterface,
)


logger = logging.getLogger(__name__)


class PDFTextExtractor(ResumeTextExtractorInterface):
    async def extract_text(self, file_path: Path) -> str:
        logger.info(
            "Starting PDF text extraction",
            extra={"file_path": str(file_path)},
        )

        if not file_path.exists():
            raise ResumeException(
                message="PDF file not found.",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ResumeErrorCode.FILE_NOT_FOUND,
            )

        if file_path.suffix.lower() != ".pdf":
            raise ResumeException(
                message="Invalid file type. Only PDF files are supported.",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ResumeErrorCode.INVALID_FILE_TYPE,
            )

        try:
            with fitz.open(file_path) as doc:
                if doc.page_count == 0:
                    raise ResumeException(
                        message="PDF file has no pages.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                        error_code=ResumeErrorCode.EMPTY_PDF,
                    )

                pages_text: list[str] = []

                for page_number, page in enumerate(doc, start=1):
                    page_text = page.get_text("text").strip()

                    if page_text:
                        pages_text.append(page_text)

                    logger.debug(
                        "Extracted text from PDF page",
                        extra={
                            "file_path": str(file_path),
                            "page_number": page_number,
                            "characters": len(page_text),
                        },
                    )

                extracted_text = "\n\n".join(pages_text).strip()

                if not extracted_text:
                    raise ResumeException(
                        message="No readable text found in PDF. This may be a scanned PDF.",
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        error_code=ResumeErrorCode.NO_READABLE_TEXT_FOUND,
                    )

                logger.info(
                    "PDF text extracted successfully",
                    extra={
                        "file_path": str(file_path),
                        "pages": doc.page_count,
                        "characters": len(extracted_text),
                    },
                )

                return extracted_text

        except ResumeException:
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error while extracting PDF text",
                extra={"file_path": str(file_path)},
            )

            raise ResumeException(
                message="Failed to extract text from PDF.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ResumeErrorCode.PDF_TEXT_EXTRACTION_FAILED,
            ) from exc