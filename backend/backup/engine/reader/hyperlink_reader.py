from __future__ import annotations

import logging

from docx.text.run import Run as DocxRun


logger = logging.getLogger(__name__)


class HyperlinkReader:
    """
    Extracts hyperlink information from a Word Run.

    Responsibilities:
        - Detect whether a run belongs to a hyperlink.
        - Resolve hyperlink relationship.
        - Return target URL.

    This reader:
        - Never modifies the document.
        - Does not handle writing.
        - Does not validate URLs.
    """

    HYPERLINK_TAG = (
        "{http://schemas.openxmlformats.org/"
        "wordprocessingml/2006/main}hyperlink"
    )

    RELATIONSHIP_ID = (
        "{http://schemas.openxmlformats.org/"
        "officeDocument/2006/relationships}id"
    )

    @staticmethod
    def read(
        run: DocxRun,
    ) -> str | None:
        """
        Extract hyperlink URL from a DOCX run.

        Returns:
            URL string if hyperlink exists.
            None otherwise.
        """

        try:

            element = run._element

            parent = element.getparent()

            if parent is None:
                return None


            # Check parent hyperlink element

            if parent.tag != HyperlinkReader.HYPERLINK_TAG:

                return None


            relationship_id = parent.get(
                HyperlinkReader.RELATIONSHIP_ID
            )

            if relationship_id is None:
                return None


            relationship = run.part.rels.get(
                relationship_id
            )

            if relationship is None:
                return None


            return str(
                relationship.target_ref
            )


        except Exception:

            logger.exception(
                "Failed to extract hyperlink from run."
            )

            return None