from __future__ import annotations

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)


class DocumentBuilder:
    """
    Applies optimization results to the
    in-memory document.

    This class never writes DOCX files.
    """

    # --------------------------------------------------

    def build(
        self,
        result: OptimizationResult,
    ) -> Document:

        document = result.document

        rewrite_map = {

            rewrite.paragraph_id: rewrite

            for rewrite in result.rewrites

        }

        for paragraph in document.paragraphs:

            rewrite = rewrite_map.get(
                paragraph.id,
            )

            if rewrite is None:

                continue

            if not paragraph.runs:

                continue

            paragraph.runs[0].text = (
                rewrite.optimized_text
            )

            for run in paragraph.runs[1:]:

                run.text = ""

        return document
