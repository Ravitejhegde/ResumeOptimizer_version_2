from __future__ import annotations

import logging

from app.engine.writer.models.paragraph_mapping import (
    ParagraphMapping,
)

from app.engine.writer.models.run_type import (
    RunType,
)


logger = logging.getLogger(__name__)


class RunDistributor:
    """
    Distributes optimized text across DOCX runs.

    Pipeline:

        RewriteResult
              |
              v
        ParagraphMapping
              |
              v
        RunDistributor
              |
              v
        DOCX Runs


    Responsibilities:

        - Replace editable text safely.
        - Preserve run structure.
        - Protect hyperlinks.
        - Avoid modifying protected runs.


    Does NOT:

        - Generate text.
        - Decide optimization.
        - Change paragraph layout.
    """



    def distribute(
        self,
        paragraph: ParagraphMapping,
    ) -> None:
        """
        Apply optimized text to editable runs.
        """

        if paragraph.rewrite is None:

            logger.debug(
                "[RunDistributor] "
                "No rewrite paragraph=%s",
                paragraph.model_paragraph.id,
            )

            return



        if not paragraph.editable:

            logger.debug(
                "[RunDistributor] "
                "Locked paragraph=%s",
                paragraph.model_paragraph.id,
            )

            return



        optimized_text = (
            paragraph.rewrite.optimized_text
        )



        if not optimized_text.strip():

            logger.warning(
                "[RunDistributor] "
                "Empty optimized text paragraph=%s",

                paragraph.model_paragraph.id,
            )

            return



        editable_runs = [

            run

            for run in paragraph.run_mappings

            if (
                run.run_type == RunType.TEXT
                and run.editable
            )

        ]



        if not editable_runs:

            logger.warning(

                "[RunDistributor] "
                "No editable runs paragraph=%s",

                paragraph.model_paragraph.id,

            )

            return



        self._apply_text(

            editable_runs,

            optimized_text,

        )



        logger.info(

            "[RunDistributor] "
            "Updated paragraph=%s editable_runs=%s",

            paragraph.model_paragraph.id,

            len(editable_runs),

        )



    # --------------------------------------------------

    def _apply_text(
        self,
        editable_runs,
        text: str,
    ) -> None:
        """
        Distribute text without removing
        run objects.

        Strategy:

        - Put text into first editable run.
        - Keep remaining runs empty.
        - Preserve formatting containers.
        """



        first_run = editable_runs[0]


        first_run.docx_run.text = text



        for run in editable_runs[1:]:

            run.docx_run.text = ""



    # --------------------------------------------------

    def can_modify(
        self,
        run,
    ) -> bool:
        """
        Safety check before modifying run.
        """


        return (

            run.editable

            and

            run.run_type == RunType.TEXT

        )