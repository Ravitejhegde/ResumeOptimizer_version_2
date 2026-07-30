from __future__ import annotations


from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)

from app.engine.models.planner.section_plan import (
    SectionPlan,
)



class SectionPlanMerger:
    """
    Merges duplicate section plans.

    Example:

    experience + experience

          ↓

    one experience section
    """


    def merge(
        self,
        plan: OptimizationPlan,
    ) -> OptimizationPlan:


        merged: dict[str, SectionPlan] = {}


        for section in plan.sections:


            if section.section not in merged:

                merged[
                    section.section
                ] = SectionPlan(

                    section=section.section,

                    editable=section.editable,

                    selected=section.selected,

                    priority=section.priority,

                    confidence=section.confidence,

                    technologies=[],

                    paragraphs=[],

                    preserve_formatting=True,

                    notes=[],

                    warnings=[],

                )


            target = merged[
                section.section
            ]


            target.technologies.extend(
                section.technologies
            )


            target.paragraphs.extend(
                section.paragraphs
            )


            target.notes.extend(
                section.notes
            )


            target.warnings.extend(
                section.warnings
            )


        plan.sections = list(
            merged.values()
        )


        return plan