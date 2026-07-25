from docx.text.paragraph import Paragraph

from app.services.document.models.hyperlink_model import (
    HyperlinkModel,
)


class HyperlinkWriter:
    """
    Writes hyperlinks back into DOCX.

    NOTE:
    python-docx has no public API for creating hyperlinks.
    This writer will inject the required XML.
    """

    @classmethod
    def write(
        cls,
        paragraph: Paragraph,
        hyperlinks: list[HyperlinkModel],
    ) -> None:
        pass