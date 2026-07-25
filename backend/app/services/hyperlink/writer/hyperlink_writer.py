from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)

from .relationship_writer import (
    RelationshipWriter,
)

from .xml_writer import (
    XmlWriter,
)


class HyperlinkWriter:
    """
    Writes hyperlinks back into a paragraph.

    Responsibilities:
    - Restore relationships
    - Restore hyperlink XML
    - Preserve formatting
    """

    @classmethod
    def write(
        cls,
        paragraph: Paragraph,
        hyperlinks: list[Hyperlink],
    ) -> None:

        if not hyperlinks:
            return

        for hyperlink in hyperlinks:

            RelationshipWriter.restore(
                paragraph,
                hyperlink,
            )

            XmlWriter.restore(
                paragraph,
                hyperlink,
            )