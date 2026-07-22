from .gap_analyzer import (
    GapAnalyzer,
)

from .priority_engine import (
    PriorityEngine,
)

from .recommendation_engine import (
    RecommendationEngine,
)

from .risk_engine import (
    RiskEngine,
)

from .models import (
    ReasoningResult,
)


class ReasoningEngine:
    """
    Compares ResumeKnowledge with
    Job Description knowledge.
    """

    @classmethod
    def analyze(
        cls,
        knowledge,
        job_description,
    ) -> ReasoningResult:

        # ----------------------------------------
        # Resume Technologies
        # ----------------------------------------

        resume_skills = set(
            knowledge.technologies
        )

        # ----------------------------------------
        # JD Technologies
        #
        # Replace this later with JDKnowledge
        # ----------------------------------------

        jd_skills = set()

        for technology in knowledge.technologies:

            if technology.lower() in job_description.lower():

                jd_skills.add(
                    technology
                )

        # ----------------------------------------
        # Gap Analysis
        # ----------------------------------------

        matched, missing, extra = GapAnalyzer.analyze(
            resume_skills,
            jd_skills,
        )

        # ----------------------------------------
        # Priority
        # ----------------------------------------

        for gap in missing:

            gap.priority = PriorityEngine.score(
                gap
            )

        # ----------------------------------------
        # Risks
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