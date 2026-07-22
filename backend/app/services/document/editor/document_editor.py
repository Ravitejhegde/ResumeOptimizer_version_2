from docx import Document

from app.services.document.editor.paragraph_editor import (
    ParagraphEditor,
)

from app.services.document.editor.paragraph_mapper import (
    ParagraphMapper,
)


class DocumentEditor:
    """
    Edits an existing DOCX document while preserving
    the document structure.
    """

    @classmethod
    def edit(
        cls,
        input_file: str,
        output_file: str,
        paragraph_updates: dict,
    ) -> None:

        document = Document(input_file)

        mapping = ParagraphMapper.map(
            document
        )

        for paragraph_id, new_text in paragraph_updates.items():

            paragraph = mapping.get(
                paragraph_id
            )

            if paragraph is None:
                continue

            ParagraphEditor.replace(
                paragraph,
                new_text,
            )

        document.save(output_file)