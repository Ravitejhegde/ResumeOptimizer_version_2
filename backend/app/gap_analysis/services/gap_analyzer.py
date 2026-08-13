"""
app.gap_analysis.services.gap_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyzes the gap between a resume and a job description.
"""

from __future__ import annotations

from app.gap_analysis.matchers.gap_score_calculator import (
    GapScoreCalculator,
)
from app.gap_analysis.matchers.role_matcher import (
    RoleMatcher,
)
from app.gap_analysis.matchers.skill_matcher import (
    SkillMatcher,
)
from app.gap_analysis.matchers.technology_matcher import (
    TechnologyMatcher,
)
from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class GapAnalyzer:
    """
    Compares resume understanding against job understanding.
    """

    def __init__(self) -> None:

        self._skills = SkillMatcher()
        self._technologies = TechnologyMatcher()
        self._roles = RoleMatcher()
        self._score = GapScoreCalculator()

    def analyze(
        self,
        resume: ResumeUnderstanding,
        job: JobUnderstanding,
    ) -> GapAnalysisModel:
        """
        Produce a GapAnalysisModel.
        """

        result = GapAnalysisModel()

        # ---------------------------------
        # Skills
        # ---------------------------------

        matched_skills, missing_skills = (
            self._skills.match(
                set(resume.primary_skills),
                set(job.required_skills),
            )
        )

        result.matched_skills = sorted(
            matched_skills
        )

        result.missing_skills = sorted(
            missing_skills
        )

        # ---------------------------------
        # Technologies
        # ---------------------------------

        (
            matched_technologies,
            missing_technologies,
        ) = self._technologies.match(
            set(resume.primary_technologies),
            set(job.required_technologies),
        )

        result.matched_technologies = sorted(
            matched_technologies
        )

        result.missing_technologies = sorted(
            missing_technologies
        )

        # ---------------------------------
        # Role
        # ---------------------------------

        result.role_match = self._roles.match(
            {
                resume.primary_role,
                *resume.secondary_roles,
            },
            job.target_role,
        )

                # ---------------------------------
        # Overall Score
        # ---------------------------------

        matched_total = (
            len(matched_skills)
            + len(matched_technologies)
        )

        required_total = (
            len(job.required_skills)
            + len(job.required_technologies)
        )

        result.overall_match = (
            self._score.calculate(
                matched_total,
                required_total,
            )
        )

        return result