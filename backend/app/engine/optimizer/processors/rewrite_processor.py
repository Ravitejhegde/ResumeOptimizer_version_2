from __future__ import annotations

from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


class RewriteProcessor:
    """
    Converts optimized text into a rewrite result.

    AI will generate the optimized text.
    This processor records the result.
    """

    # --------------------------------------------------

    def process(
        self,
        paragraph: Paragraph,
        optimized_text: str,
        reason: str = "",
    ) -> RewriteResult:

        return RewriteResult(

            paragraph_id=paragraph.id,

            success=(
                paragraph.text != optimized_text
            ),

            original_text=paragraph.text,

            optimized_text=optimized_text,

            reason=reason,

        )
