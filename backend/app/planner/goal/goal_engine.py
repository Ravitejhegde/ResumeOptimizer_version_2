"""
app.planner.goal.goal_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds an OptimizationGoal from resume and job understanding.
"""

from __future__ import annotations

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)
from app.planner.goal.optimization_goal import (
    OptimizationGoal,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class GoalEngine:
    """
    Determines the optimization objective.
    """

    def build(
        self,
        resume: ResumeUnderstanding,
        job: JobUnderstanding,
        gap: GapAnalysisModel,
    ) -> OptimizationGoal:

        goal = OptimizationGoal()

        # ------------------------------------
        # Role information
        # ------------------------------------

        goal.current_role = (
            resume.primary_role
        )

        goal.target_role = (
            job.target_role
        )

        goal.target_skills = list(
            job.required_skills
        )

        goal.target_technologies = list(
            job.required_technologies
        )

        goal.matched_roles = [
            resume.primary_role
        ]

        # ------------------------------------
        # Decide objective
        # ------------------------------------

        if (
            resume.primary_role
            == job.target_role
        ):

            if gap.overall_match >= 0.80:

                goal.objective = (
                    "ATS Improvement"
                )

                goal.optimization_level = (
                    "minor"
                )

            elif gap.overall_match >= 0.50:

                goal.objective = (
                    "Resume Enhancement"
                )

                goal.optimization_level = (
                    "moderate"
                )

            else:

                goal.objective = (
                    "Major Resume Rewrite"
                )

                goal.optimization_level = (
                    "major"
                )

        else:

            goal.objective = (
                "Role Transition"
            )

            goal.optimization_level = (
                "aggressive"
            )

        # ------------------------------------
        # Notes
        # ------------------------------------

        if gap.missing_skills:

            goal.notes.append(
                f"{len(gap.missing_skills)} "
                "important skills missing."
            )

        if gap.missing_technologies:

            goal.notes.append(
                f"{len(gap.missing_technologies)} "
                "technologies missing."
            )

        return goal