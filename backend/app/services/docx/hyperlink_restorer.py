from app.core.logger import logger

from .hyperlink_xml import (
    HyperlinkXML,
)

from .relationship_manager import (
    RelationshipManager,
)

from .hyperlink_utils import (
    HyperlinkUtils,
)

from .hyperlink_xml_writer import (
    HyperlinkXMLWriter,
)


class HyperlinkRestorer:
    """
    Restores hyperlinks into an existing paragraph.

    Current version:
    - Detects hyperlinks
    - Reads existing hyperlink XML
    - Logs hyperlink information

    Future versions will restore:
    - Relationship IDs
    - URLs
    - Email links
    - Bookmarks
    - Hyperlink formatting
    """

    @classmethod
    def restore(
        cls,
        paragraph,
        hyperlinks,
    ) -> None:

        if not hyperlinks:
            return

        # -----------------------------------------
        # Read existing hyperlink XML
        # -----------------------------------------

        xml_links = HyperlinkXML.find_all(
            paragraph
        )

        logger.info(
            f"Original XML hyperlinks: {len(xml_links)}"
        )

        # -----------------------------------------
        # Log hyperlink information
        # -----------------------------------------

        for link in hyperlinks:

            if not HyperlinkUtils.is_valid(
                link
            ):
                continue

            resolved = RelationshipManager.get_url(
                paragraph,
                link.relationship_id,
            )

            logger.info(
                f"Text : {link.text}"
            )

            logger.info(
                f"Saved URL : {HyperlinkUtils.normalize(link.url)}"
            )

            logger.info(
                f"Resolved URL : {resolved}"
            )

        # -----------------------------------------
        # XML restoration
        # (Placeholder for next phase)
        # -----------------------------------------

        HyperlinkXMLWriter.restore(
            source_paragraph=paragraph,
            target_paragraph=paragraph,
        )