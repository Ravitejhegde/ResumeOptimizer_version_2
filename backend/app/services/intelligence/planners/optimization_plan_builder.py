from app.services.intelligence.models import (
    OptimizationPlan,
)


class OptimizationPlanBuilder:
    """
    Temporary V3 planner.

    Builds an optimization plan from
    ResumeKnowledge until the advanced
    planner is migrated.
    """

    @classmethod
    def build(
        cls,
        knowledge,
        job_description,
    ) -> OptimizationPlan:

        jd_lower = job_description.lower()

        keep = []
        add = []
        remove = []

        for technology in knowledge.technologies:

            if technology.lower() in jd_lower:

                keep.append(technology)

            else:

                remove.append(technology)

        for technology in knowledge.technologies:

            if technology.lower() in jd_lower:

                continue

        return OptimizationPlan(

            source_role=knowledge.detected_role,

            target_role="Unknown",

            keep=keep,

            remove=remove,

            add=add,

            warnings=[],

        )