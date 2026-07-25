from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)

from .hyperlink_text_editor import (
    HyperlinkTextEditor,
)

from .hyperlink_run_editor import (
    HyperlinkRunEditor,
)


class HyperlinkEditor:
    """
    Coordinates all hyperlink editing operations.

    This class never changes the hyperlink URL.
    It only updates display text and formatting
    while preserving the original hyperlink.
    """

    @classmethod
    def update(
        cls,
        paragraph: Paragraph,
        hyperlink: Hyperlink,
        new_text: str,
    ) -> None:

        # Update displayed text
        HyperlinkTextEditor.update(
            paragraph=paragraph,
            hyperlink=hyperlink,
            new_text=new_text,
        )

        # Restore run formatting
        HyperlinkRunEditor.restore(
            paragraph=paragraph,
            hyperlink=hyperlink,
        )