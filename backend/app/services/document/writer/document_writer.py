from docx import Document

from app.services.document.models.document_model import (
    DocumentModel,
)

from app.services.document.writer.section_writer import (
    SectionWriter,
)


class DocumentWriter:
    """
    Writes a DocumentModel back to DOCX.

    This class is only responsible for
    orchestration.
    """

    @classmethod
    def write(
        cls,
        model: DocumentModel,
        output_file: str,
    ) -> None:

        document = Document()

        # -----------------------------------------
        # Core Properties
        # -----------------------------------------

        properties = document.core_properties

        properties.title = model.title

        properties.author = model.author

        properties.subject = model.subject

        properties.keywords = ",".join(
            model.keywords
        )

        # -----------------------------------------
        # Sections
        # -----------------------------------------

        SectionWriter.write(
            document,
            model.sections,
        )

        # -----------------------------------------
        # Save
        # -----------------------------------------

        document.save(
            output_file
        )