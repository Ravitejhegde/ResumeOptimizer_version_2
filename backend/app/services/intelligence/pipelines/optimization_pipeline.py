from app.services.intelligence.pipelines.resume_pipeline import (
    ResumePipeline,
)

from app.services.intelligence.pipelines.jd_pipeline import (
    JDPipeline,
)

from app.services.intelligence.planners.optimization_plan_builder import (
    OptimizationPlanBuilder,
)

from app.services.intelligence.planners.warning_builder import (
    WarningBuilder,
)


class OptimizationPipeline:
    """
    Main intelligence pipeline.

    Resume
        ↓
    Resume Knowledge

    Job Description
        ↓
    JD Knowledge

    Resume + JD
        ↓
    Optimization Plan
    """

    @classmethod
    def run(
        cls,
        blocks,
        job_description,
        selected_skills,
    ):

        # -----------------------------
        # Resume Knowledge
        # -----------------------------

        resume = ResumePipeline.run(
            blocks
        )

        # -----------------------------
        # JD Knowledge
        # -----------------------------

        jd = JDPipeline.run(
            job_description
        )

        # -----------------------------
        # Build Optimization Plan
        # -----------------------------

        plan = OptimizationPlanBuilder.build(
            resume,
            jd,
            selected_skills,
        )

        # -----------------------------
        # Warnings
        # -----------------------------

        plan.warnings = WarningBuilder.build(
            resume,
            jd,
            plan,
        )

        return plan