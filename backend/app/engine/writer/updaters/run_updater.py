from __future__ import annotations

import logging

from app.engine.writer.models.write_context import (
    WriteContext,
)

from app.engine.writer.updaters.run_distributor import (
    RunDistributor,
)


logger = logging.getLogger(__name__)


class RunUpdater:
    """
    Applies rewrite changes at run level.

    Pipeline:

        ParagraphMapping
              |
              v
          RunUpdater
              |
              v
        RunDistributor
              |
              v
          DOCX Runs


    Responsibilities:

        - Process editable paragraphs.
        - Forward rewrite data.
        - Preserve run structure.

    Does NOT:

        - Generate text.
        - Analyze resume.
        - Decide optimization.
        - Handle paragraph matching.
    """


    def __init__(
        self,
    ) -> None:

        self._distributor = RunDistributor()



    # --------------------------------------------------

    def update(
        self,
        context: WriteContext,
    ) -> None:
        """
        Update editable runs.
        """


        if not context.paragraph_mappings:

            logger.info(
                "[RunUpdater] "
                "No paragraph mappings."
            )

            return



        updated = 0



        for mapping in context.paragraph_mappings:



            # ----------------------------------
            # Skip locked paragraphs
            # ----------------------------------

            if not mapping.editable:

                continue



            # ----------------------------------
            # Skip paragraphs without rewrite
            # ----------------------------------

            if mapping.rewrite is None:

                continue



            if not mapping.rewrite.success:

                logger.debug(
                    "[RunUpdater] "
                    "Skipping unsuccessful rewrite "
                    "paragraph=%s",
                    mapping.model_paragraph.id,
                )

                continue



            # ----------------------------------
            # Apply rewrite
            # ----------------------------------

            self._distributor.distribute(
                mapping,
            )


            updated += 1



            logger.info(

                "[RunUpdater] "
                "Updated paragraph=%s",

                mapping.model_paragraph.id,

            )



        logger.info(
            "[RunUpdater] "
            "Total updated paragraphs=%s",
            updated,
        )