from __future__ import annotations

from collections import defaultdict

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)

from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


class RewritePlanBuilder:
    """
    Builds paragraph-level rewrite instructions.

    Flow:

        SectionPlan
              |
              v
        RewritePlan


    Responsibilities:

        - Group technologies by paragraph.
        - Avoid duplicate rewrite tasks.
        - Create controlled rewrite instructions.
        - Keep one rewrite per paragraph.


    Does NOT:

        - Generate text.
        - Modify DOCX.
        - Call AI.
    """



    def build(
        self,
        plan: OptimizationPlan,
    ) -> OptimizationPlan:


        grouped: dict[
            tuple[str, str],
            list[str]
        ] = defaultdict(list)



        # ----------------------------------
        # Collect technologies per paragraph
        # ----------------------------------

        for section in plan.sections:


            if not section.editable:

                continue



            for paragraph_id in section.paragraphs:


                grouped[
                    (
                        paragraph_id,
                        section.section,
                    )
                ].extend(
                    section.technologies
                )



        rewrites: list[RewritePlan] = []



        # ----------------------------------
        # Create one rewrite per paragraph
        # ----------------------------------

        for (
            paragraph_id,
            section_name,
        ), technologies in grouped.items():


            unique_technologies = list(
                dict.fromkeys(
                    tech.strip()
                    for tech in technologies
                    if tech
                )
            )



            if not unique_technologies:

                continue



            rewrites.append(

                RewritePlan(

                    paragraph_id=paragraph_id,

                    section=section_name,

                    # Store grouped technologies
                    # for TechnologyProcessor

                    technology=", ".join(
                        unique_technologies
                    ),

                    action="promote",

                    priority=self._priority(
                        plan,
                        section_name,
                    ),

                    reason=(
                        "Technology promotion "
                        "based on job requirements"
                    ),

                    confidence=1.0,

                    preserve_formatting=True,

                )

            )



        plan.rewrites = rewrites


        return plan



    # ----------------------------------
    # Get section priority
    # ----------------------------------

    def _priority(
        self,
        plan: OptimizationPlan,
        section: str,
    ) -> int:


        for section_plan in plan.sections:


            if section_plan.section == section:

                return section_plan.priority



        return 0