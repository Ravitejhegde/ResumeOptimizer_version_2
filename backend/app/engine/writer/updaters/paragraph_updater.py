from __future__ import annotations

import logging

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class ParagraphUpdater:
    """
    Connects optimization rewrites
    with document paragraph mappings.

    Flow:

    OptimizationResult
            |
            v
    ParagraphUpdater
            |
            v
    ParagraphMapping
            |
            v
    RunUpdater


    Responsibilities:
        - Find matching paragraph.
        - Attach rewrite object.
        - Mark editable state.

    Does NOT:
        - Change paragraph text.
        - Change runs.
        - Handle DOCX writing.
    """

    def update(
        self,
        context: WriteContext,
    ) -> None:
        """
        Attach rewrite instructions
        to paragraph mappings.
        """


        rewrites = (
            context.optimization.rewrites
        )


        if not rewrites:

            logger.info(
                "[ParagraphUpdater] "
                "No rewrites available."
            )

            return



        # ----------------------------------
        # Build rewrite lookup
        # ----------------------------------

        rewrite_map = {

            rewrite.paragraph_id: rewrite

            for rewrite in rewrites

        }



        # ----------------------------------
        # Match paragraphs
        # ----------------------------------

        for mapping in context.paragraph_mappings:


            paragraph_id = (
                mapping.model_paragraph.id
            )


            rewrite = (
                rewrite_map.get(
                    paragraph_id
                )
            )



            if rewrite is None:


                mapping.editable = False


                logger.debug(

                    "[ParagraphUpdater] "
                    "Paragraph=%s ID=%s Rewrite=NO",

                    mapping.paragraph_index,

                    paragraph_id,

                )


                continue



            # Attach rewrite

            mapping.rewrite = rewrite


            mapping.editable = True



            logger.info(

                "[ParagraphUpdater] "
                "Paragraph=%s ID=%s Rewrite=YES",

                mapping.paragraph_index,

                paragraph_id,

            )