from __future__ import annotations

from app.engine.models.document.document import Document
from app.engine.reader.section_reader import SectionReader


class SnapshotBuilder:
    """
    Finalizes the in-memory document after it has been
    read by the Reader module.

    Responsibilities
    ----------------
    - Detect logical resume sections.
    - Populate derived properties.
    - Validate internal consistency.
    - Never modify original document formatting.
    """

    @staticmethod
    def build(
        document: Document,
    ) -> Document:

        current_section = None

        # ----------------------------------------
        # Detect Sections
        # ----------------------------------------

        for paragraph in document.paragraphs:

            detected = SectionReader.detect(
                paragraph
            )

            if detected.value != "unknown":

                current_section = detected.value

            paragraph.section = current_section

        # ----------------------------------------
        # Derived Metadata
        # ----------------------------------------

        document.page_count = max(
            document.page_count,
            1,
        )

        return document




