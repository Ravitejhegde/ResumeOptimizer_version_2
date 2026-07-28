from __future__ import annotations

from app.engine.models.document.paragraph import (
    Paragraph,
)


class StylePreserver:
    """
    Ensures character and paragraph styles remain
    unchanged after optimization.

    This class performs validation only.
    """

    # --------------------------------------------------

    def preserve(
        self,
        original: Paragraph,
        updated: Paragraph,
    ) -> Paragraph:

        if len(original.runs) != len(updated.runs):

            return original

        for original_run, updated_run in zip(
            original.runs,
            updated.runs,
        ):

            updated_run.style = original_run.style

            updated_run.hyperlink = (
                original_run.hyperlink
            )

            updated_run.editable = (
                original_run.editable
            )

            updated_run.locked_reason = (
                original_run.locked_reason
            )

        updated.style_name = original.style_name

        updated.alignment = original.alignment

        updated.left_indent = original.left_indent

        updated.right_indent = original.right_indent

        updated.first_line_indent = (
            original.first_line_indent
        )

        updated.space_before = (
            original.space_before
        )

        updated.space_after = (
            original.space_after
        )

        updated.line_spacing = (
            original.line_spacing
        )

        updated.keep_together = (
            original.keep_together
        )

        updated.keep_with_next = (
            original.keep_with_next
        )

        updated.page_break_before = (
            original.page_break_before
        )

        return updated
