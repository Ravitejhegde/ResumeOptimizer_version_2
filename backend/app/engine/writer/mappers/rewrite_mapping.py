from __future__ import annotations

import logging

from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)

from app.engine.writer.models.paragraph_mapping import (
    ParagraphMapping,
)


logger = logging.getLogger(__name__)


class RewriteMapping:
    """
    Maps AI rewrite results to Writer paragraph mappings.

    Flow:

        OptimizationResult
              |
              v

        RewriteResult[]

              |
              v

        RewriteMapping

              |
              v

        ParagraphMapping

              |
              v

        RunUpdater


    Responsibilities:

        - Match AI paragraph ids with DOCX paragraphs.
        - Attach rewrite instructions.
        - Prepare Writer context.


    Does NOT:

        - Modify DOCX text.
        - Generate content.
        - Handle formatting.
    """



    def apply(
        self,
        rewrites: list[RewriteResult],
        paragraphs: list[ParagraphMapping],
    ) -> None:
        """
        Attach rewrite results to paragraph mappings.
        """


        if not rewrites:

            logger.warning(
                "[RewriteMapping] "
                "No rewrites received."
            )

            return



        paragraph_index = {

            self._normalize(
                paragraph.model_paragraph.id
            ):
            paragraph

            for paragraph in paragraphs

        }



        mapped = 0



        for rewrite in rewrites:


            paragraph_id = (
                self._normalize(
                    rewrite.paragraph_id
                )
            )


            paragraph = (
                paragraph_index.get(
                    paragraph_id
                )
            )


            if paragraph is None:


                logger.warning(

                    "[RewriteMapping] "
                    "Paragraph not found id=%s",

                    rewrite.paragraph_id,

                )

                continue



            paragraph.rewrite = rewrite

            mapped += 1



        logger.info(

            "[RewriteMapping] "
            "Mapped rewrites=%s/%s",

            mapped,

            len(rewrites),

        )



    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(
        value: str | None,
    ) -> str:
        """
        Normalize ids safely.
        """

        if not value:

            return ""


        return (
            str(value)
            .strip()
            .lower()
        )