from __future__ import annotations

from app.engine.models.document.document import (
    Document,
)


class LayoutPreserver:
    """
    Ensures document layout remains unchanged.

    This class never modifies content.
    It only restores layout-related properties.
    """

    # --------------------------------------------------

    def preserve(
        self,
        original: Document,
        updated: Document,
    ) -> Document:

        updated.page_count = (
            original.page_count
        )

        updated.section_count = (
            original.section_count
        )

        updated.source_path = (
            original.source_path
        )

        for original_paragraph, updated_paragraph in zip(
            original.paragraphs,
            updated.paragraphs,
        ):

            updated_paragraph.layout_budget = (
                original_paragraph.layout_budget
            )

            updated_paragraph.section = (
                original_paragraph.section
            )

        return updated
