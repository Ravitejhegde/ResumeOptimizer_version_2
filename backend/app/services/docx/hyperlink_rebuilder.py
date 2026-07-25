from app.core.logger import logger

from .hyperlink_xml import HyperlinkXML
from .hyperlink_xml_writer import HyperlinkXMLWriter
from .relationship_writer import RelationshipWriter


class HyperlinkRebuilder:
    """
    Coordinates complete hyperlink restoration.

    Pipeline:

    Original Paragraph
            │
            ▼
    Read Hyperlink XML
            │
            ▼
    Copy Relationships
            │
            ▼
    Restore Hyperlink XML
            │
            ▼
    Restore Styles
    """

    @classmethod
    def rebuild(
        cls,
        source_paragraph,
        target_paragraph,
    ) -> None:

        if not HyperlinkXML.has_hyperlinks(
            source_paragraph
        ):
            return

        logger.info(
            "Rebuilding hyperlinks..."
        )

        RelationshipWriter.copy_relationships(
            source_paragraph,
            target_paragraph,
        )

        HyperlinkXMLWriter.restore(
            source_paragraph,
            target_paragraph,
        )