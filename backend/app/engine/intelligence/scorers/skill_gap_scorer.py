from __future__ import annotations

from app.engine.models.analysis.analysis_result import (
    AnalysisResult,
)
from app.engine.models.intelligence.skill_gap import (
    SkillGap,
)
from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


class SkillGapScorer:
    """
    Builds a SkillGap model from
    analysis results.
    """

    def score(
        self,
        analysis: AnalysisResult,
    ) -> SkillGap:

        matched = [
            SkillPriority(
                technology=skill,
                category="",
                priority=100,
                matched=True,
            )
            for skill in analysis.comparison.matched
        ]

        missing = [
            SkillPriority(
                technology=skill,
                category="",
                priority=100,
                matched=False,
            )
            for skill in analysis.comparison.missing
        ]

        return SkillGap(

            matched=matched,

            missing=missing,

            additional=analysis.comparison.extra,

            score=analysis.comparison.score,

        )
