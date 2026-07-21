from app.services.document.editor.document_editor import (
    DocumentEditor,
)


class EditorPipeline:
    """
    Applies AI paragraph updates to
    an existing DOCX document.
    """

    @classmethod
    def apply(
        cls,
        input_file: str,
        output_file: str,
        paragraph_updates: dict[int, str],
    ) -> None:

        DocumentEditor.edit(
            input_file=input_file,
            output_file=output_file,
            paragraph_updates=paragraph_updates,
        )