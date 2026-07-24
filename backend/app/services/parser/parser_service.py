from pathlib import Path

from app.services.parser.docx_parser import DocxParser
from app.services.parser.models import ResumeDocument


class ParserService:
    """
    Commercial Resume Parser.

    Supported:
    - DOCX
    - Formatting
    - Paragraphs
    - Tables
    - Headings
    - Statistics

    Future:
    - PDF
    - OCR
    """

    @staticmethod
    def parse_resume(
        file_path: str,
    ) -> ResumeDocument:

        extension = (
            Path(file_path)
            .suffix
            .lower()
        )

        if extension != ".docx":
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return DocxParser.parse(
            file_path=file_path,
        )