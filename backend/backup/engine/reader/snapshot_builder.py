from __future__ import annotations

import logging

from app.engine.models.document.document import (
    Document,
)
from app.engine.reader.section_reader import (
    SectionReader,
)


logger = logging.getLogger(__name__)


class SnapshotBuilder:
    """
    Finalizes the in-memory document after reading.

    Responsibilities:
        - Detect logical resume sections.
        - Populate derived metadata.
        - Validate document consistency.
        - Prepare canonical engine snapshot.

    Does NOT:
        - Modify DOCX.
        - Rewrite text.
        - Change formatting.
    """


    @staticmethod
    def build(
        document: Document,
    ) -> Document:
        """
        Build final document snapshot.
        """

        if document is None:
            raise ValueError(
                "Document cannot be None."
            )


        current_section: str | None = None


        # ----------------------------------
        # Detect resume sections
        # ----------------------------------

        detected_sections: set[str] = set()


        for paragraph in document.paragraphs:

            detected = SectionReader.detect(
                paragraph
            )


            if detected.value != "unknown":

                current_section = (
                    detected.value
                )

                detected_sections.add(
                    current_section
                )


            paragraph.section = (
                current_section
            )


        # ----------------------------------
        # Derived metadata
        # ----------------------------------

        if document.page_count <= 0:

            document.page_count = 1


        if document.section_count <= 0:

            document.section_count = len(
                detected_sections
            )


        logger.info(
            "Snapshot built: paragraphs=%s tables=%s sections=%s",
            len(document.paragraphs),
            len(document.tables),
            document.section_count,
        )


        # ----------------------------------
        # Validate consistency
        # ----------------------------------

        SnapshotBuilder._validate(
            document
        )


        return document



    @staticmethod
    def _validate(
        document: Document,
    ) -> None:
        """
        Validate internal document state.
        """

        for paragraph in document.paragraphs:

            if not paragraph.id:

                raise ValueError(
                    "Paragraph missing ID."
                )


        for table in document.tables:

            if not table.id:

                raise ValueError(
                    "Table missing ID."
                )