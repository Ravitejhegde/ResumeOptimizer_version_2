from docx import Document

from app.services.document.models.document_model import (
    DocumentModel,
)

from app.services.document.parser.section_parser import (
    SectionParser,
)


class DocumentParser:
    """
    Master parser for DOCX documents.

    Responsible only for orchestration.

    Individual document parts are parsed by
    specialized parsers.
    """

    @classmethod
    def parse(
        cls,
        filename: str,
    ) -> DocumentModel:

        document = Document(filename)

        model = DocumentModel()

        model.filename = filename

        # -----------------------------------------
        # Core Metadata
        # -----------------------------------------

        properties = document.core_properties

        model.title = properties.title or ""

        model.author = properties.author or ""

        model.company = ""

        model.subject = properties.subject or ""

        model.keywords = (
            properties.keywords.split(",")
            if properties.keywords
            else []
        )

        # -----------------------------------------
        # Sections
        # -----------------------------------------

        model.sections = SectionParser.parse(
            document
        )

        model.page_count = len(
            model.sections
        )

        return model