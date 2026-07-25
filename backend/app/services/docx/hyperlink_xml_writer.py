from copy import deepcopy

from app.core.logger import logger

from .hyperlink_xml import (
    HyperlinkXML,
)


class HyperlinkXMLWriter:
    """
    Writes hyperlink XML back into a paragraph.

    Current version:
    - Copies existing hyperlink XML
    - Preserves relationship IDs
    - Preserves hyperlink formatting

    Future versions:
    - Update hyperlink text
    - Create new hyperlinks
    - Delete hyperlinks
    """

    @classmethod
    def restore(
        cls,
        source_paragraph,
        target_paragraph,
    ) -> None:

        hyperlinks = HyperlinkXML.find_all(
            source_paragraph
        )

        if not hyperlinks:
            return

        logger.info(
            f"Copying {len(hyperlinks)} hyperlink(s)"
        )

        for hyperlink in hyperlinks:

            target_paragraph._p.append(
                deepcopy(hyperlink)
            )