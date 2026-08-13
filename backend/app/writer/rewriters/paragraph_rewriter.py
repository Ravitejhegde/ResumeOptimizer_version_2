"""
app.writer.rewriters.paragraph_rewriter

Applies optimized content to DOCX paragraphs.
"""

from __future__ import annotations

from app.optimizer.models.paragraph_update import (
    ParagraphUpdate,
)

from app.writer.analyzers.paragraph_locator import (
    ParagraphLocator,
)

from app.writer.models.write_context import (
    WriteContext,
)

from app.writer.rewriters.run_distributor import (
    RunDistributor,
)


class ParagraphRewriter:
    """
    Rewrites document paragraphs.

    Responsibilities
    ----------------
    - Locate target paragraphs.
    - Skip unchanged paragraphs.
    - Apply optimized text.
    - Preserve formatting through RunDistributor.
    """

    def __init__(
        self,
    ) -> None:

        self._locator = ParagraphLocator()

        self._distributor = RunDistributor()

    def rewrite(
        self,
        context: WriteContext,
    ) -> None:
        """
        Apply AI-generated paragraph updates.
        """

        updates = (
            context.optimization.paragraph_updates
        )

        if not updates:
            return

        for update in updates:

            if not isinstance(
                update,
                ParagraphUpdate,
            ):
                continue

            if not update.changed:
                continue

            paragraph = (
                self._locator.get_paragraph(
                    context=context,
                    paragraph_id=update.paragraph_id,
                )
            )

            if paragraph is None:

                context.add_warning(
                    f"Paragraph '{update.paragraph_id}' not found."
                )

                continue

            self._distributor.distribute(
                paragraph=paragraph,
                text=update.optimized_text,
            )