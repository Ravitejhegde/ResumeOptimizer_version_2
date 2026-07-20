from .gap_analyzer import GapAnalyzer
from .priority_engine import PriorityEngine
from .recommendation_engine import RecommendationEngine
from .risk_engine import RiskEngine
from .models import ReasoningResult


class ReasoningEngine:
    """
    Compares Resume knowledge with JD knowledge and
    produces reasoning for optimization.
    """

    @classmethod
    def analyze(
        cls,
        resume,
        jd,
    ) -> ReasoningResult:

        # ----------------------------------------
        # Gap Analysis
        # ----------------------------------------

        matched, missing, extra = GapAnalyzer.analyze(
            resume.skills,
            jd.skills,
        )

        # ----------------------------------------
        # Priority Scoring
        # ----------------------------------------

        for gap in missing:

            gap.priority = PriorityEngine.score(
                gap
            )

        # ----------------------------------------
        # Risk Analysis
        # ----------------------------------------

        risks = RiskEngine.evaluate(
            missing
        )

        # ----------------------------------------
        # Recommendations
        # ----------------------------------------

        recommendations = RecommendationEngine.build(
            missing
        )

        # ----------------------------------------
        # Result
        # ----------------------------------------

        return ReasoningResult(
            matched=matched,
            missing=missing,
            extra=extra,
            recommendations=recommendations,
            risks=risks,
        )