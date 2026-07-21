from docx.text.paragraph import Paragraph

from app.services.document.editor.run_editor import (
    RunEditor,
)


class ParagraphEditor:
    """
    Edits an existing Word paragraph while
    preserving its formatting.
    """

    @classmethod
    def replace(
        cls,
        paragraph: Paragraph,
        optimized_text: str,
    ) -> None:

        # Nothing to edit
        if not paragraph.runs:
            return

        RunEditor.replace(
            paragraph.runs,
            optimized_text,
        )