from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.optimizer.text_optimizer import (
    TextOptimizer,
)

from app.services.ai.batch.batch_models import (
    BatchRewriteResult,
)


class AIResponseApplier:
    """
    Applies AI rewrite results to the document.

    Responsibilities
    ----------------
    • Match paragraph IDs
    • Apply rewritten text
    • Preserve formatting

    Never calls AI.
    """

    @staticmethod
    def apply(
        document: Document,
        result: BatchRewriteResult,
    ) -> Document:

        paragraph_lookup = {

            paragraph.id: paragraph

            for paragraph in document.paragraphs

        }

        for rewritten in result.paragraphs:

            paragraph = paragraph_lookup.get(
                rewritten.id
            )

            if paragraph is None:
                continue

            TextOptimizer.apply(

                paragraph=paragraph,

                optimized_text=rewritten.text,

            )

        return document