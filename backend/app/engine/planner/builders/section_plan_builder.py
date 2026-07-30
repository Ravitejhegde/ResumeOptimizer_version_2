from __future__ import annotations

import logging

from app.engine.models.document.document import (
    Document,
)

from app.engine.models.intelligence.promotion_plan import (
    PromotionPlan,
)

from app.engine.models.planner.section_plan import (
    SectionPlan,
)


logger = logging.getLogger(__name__)


class SectionPlanBuilder:
    """
    Creates section-level optimization plans.

    Flow:

        PromotionPlan
              +
        Document Snapshot

              |
              v

        SectionPlan


    Responsibilities:

        - Group technologies by section.
        - Attach paragraph IDs.
        - Avoid duplicate sections.
        - Preserve document structure.


    Does NOT:

        - Rewrite content.
        - Generate text.
        - Modify DOCX.
    """

    def build(
        self,
        promotion_plan: PromotionPlan,
        document: Document,
    ) -> list[SectionPlan]:

        grouped: dict[str, SectionPlan] = {}


        for decision in promotion_plan.decisions:


            section_name = self._normalize(
                decision.section
            )


            if not section_name:
                continue


            # -----------------------------
            # Find paragraphs only once
            # -----------------------------

            paragraph_ids = [

                paragraph.id

                for paragraph in document.paragraphs

                if self._normalize(
                    paragraph.section
                )
                == section_name

            ]


            # -----------------------------
            # Create section bucket
            # -----------------------------

            if section_name not in grouped:


                grouped[section_name] = SectionPlan(

                    section=section_name,

                    editable=True,

                    selected=True,

                    priority=decision.priority,

                    confidence=decision.confidence,

                    technologies=[],

                    paragraphs=paragraph_ids,

                    preserve_formatting=True,

                    notes=[
                        "Generated from promotion plan"
                    ],

                    warnings=[],

                )


            section_plan = grouped[
                section_name
            ]


            # -----------------------------
            # Merge technologies
            # -----------------------------

            if decision.technology not in section_plan.technologies:

                section_plan.technologies.append(
                    decision.technology
                )


            # Keep highest priority

            section_plan.priority = max(
                section_plan.priority,
                decision.priority,
            )


            logger.info(

                "[SectionPlanBuilder] "
                "Section=%s "
                "Technology=%s "
                "Paragraphs=%s",

                section_name,

                decision.technology,

                len(section_plan.paragraphs),

            )


        return list(
            grouped.values()
        )



    # --------------------------------------------------

    @staticmethod
    def _normalize(
        value,
    ) -> str:
        """
        Normalize section values.
        """

        if value is None:
            return ""


        text = str(value)


        if "." in text:

            text = text.split(
                "."
            )[-1]


        return (
            text
            .lower()
            .strip()
        )