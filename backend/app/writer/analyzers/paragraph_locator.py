"""
app.writer.analyzers.paragraph_locator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a mapping between DocumentModel paragraph IDs
and python-docx paragraphs.
"""

from __future__ import annotations

from docx.text.paragraph import Paragraph

from app.writer.models.write_context import (
    WriteContext,
)


class ParagraphLocator:
    """
    Creates paragraph lookup tables.

    Responsibilities
    ----------------
    - Match DocumentModel paragraphs with DOCX paragraphs.
    - Populate WriteContext.paragraph_map.
    """

    def locate(
        self,
        context: WriteContext,
    ) -> None:
        """
        Build paragraph lookup.
        """

        model_paragraphs = (
            context.document.paragraphs
        )

        docx_paragraphs = (
            context.working_document.paragraphs
        )

        count = min(
            len(model_paragraphs),
            len(docx_paragraphs),
        )

        context.paragraph_map.clear()

        for index in range(count):

            paragraph_id = (
                model_paragraphs[index].id
            )

            context.paragraph_map[
                paragraph_id
            ] = index

        if (
            len(model_paragraphs)
            != len(docx_paragraphs)
        ):
            context.add_warning(
                "Paragraph count mismatch "
                f"(model={len(model_paragraphs)}, "
                f"docx={len(docx_paragraphs)})"
            )

    def get_paragraph(
        self,
        context: WriteContext,
        paragraph_id: str,
    ) -> Paragraph | None:
        """
        Return the DOCX paragraph for a given ID.
        """

        index = context.paragraph_map.get(
            paragraph_id
        )

        if index is None:
            return None

        return (
            context.working_document
            .paragraphs[index]
        )