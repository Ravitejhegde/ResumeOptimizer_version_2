from __future__ import annotations

import logging

from app.engine.models.document.document import (
    Document,
)

from app.engine.models.planner.section_plan import (
    SectionPlan,
)


logger = logging.getLogger(__name__)


class SectionExecutor:
    """
    Executes optimization for one resume section.

    Flow:

        SectionPlan
             |
             v
        SectionExecutor
             |
             v
        Matching Paragraphs
             |
             v
        ParagraphExecutor


    Responsibilities:

        - Find paragraphs belonging to section.
        - Respect planner decisions.
        - Preserve document order.


    Does NOT:

        - Rewrite text.
        - Generate content.
        - Modify DOCX.
    """



    def execute(
        self,
        document: Document,
        plan: SectionPlan,
    ) -> list:
        """
        Return paragraphs eligible
        for optimization.
        """

        if not plan.editable:

            logger.debug(
                "[SectionExecutor] "
                "Section locked: %s",
                plan.section,
            )

            return []



        # ----------------------------------
        # Preferred method:
        # Use planner paragraph IDs
        # ----------------------------------

        if plan.paragraphs:


            paragraph_ids = set(
                plan.paragraphs
            )


            selected = [

                paragraph

                for paragraph in document.paragraphs

                if paragraph.id in paragraph_ids

            ]


            logger.info(

                "[SectionExecutor] "
                "Section=%s Paragraphs=%s "
                "(from plan IDs)",

                plan.section,

                len(selected),

            )


            return selected



        # ----------------------------------
        # Fallback:
        # Match section metadata
        # ----------------------------------

        section_name = (
            str(plan.section)
            .lower()
            .strip()
        )


        selected = []


        for paragraph in document.paragraphs:


            paragraph_section = (
                str(
                    paragraph.section
                )
                .lower()
                .strip()
            )


            if (
                paragraph_section
                == section_name
            ):

                selected.append(
                    paragraph
                )



        logger.info(

            "[SectionExecutor] "
            "Section=%s Paragraphs=%s "
            "(from section match)",

            plan.section,

            len(selected),

        )


        return selected