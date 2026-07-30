from __future__ import annotations

from app.engine.models.analysis.comparison_analysis import (
    ComparisonAnalysis,
)
from app.engine.models.analysis.jd_analysis import (
    JDAnalysis,
)
from app.engine.models.analysis.keyword_analysis import (
    KeywordAnalysis,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class SkillComparator:
    """
    Compares resume skills against the
    Job Description using the Knowledge Platform.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    # --------------------------------------------------

    def compare(
        self,
        resume: KeywordAnalysis,
        job: JDAnalysis,
    ) -> ComparisonAnalysis:

        resume_skills = set(
            resume.normalized,
        )

        jd_skills = set(
            job.required_skills,
        )

        matched = sorted(
            resume_skills & jd_skills,
        )

        missing = sorted(
            jd_skills - resume_skills,
        )

        extra = sorted(
            resume_skills - jd_skills,
        )

        related: set[str] = set()

        for skill in missing:

            related.update(
                self._knowledge.related(
                    skill,
                )
            )

        if jd_skills:

            score = round(
                (
                    len(matched)
                    / len(jd_skills)
                )
                * 100,
                2,
            )

        else:

            score = 100.0

        return ComparisonAnalysis(

            matched=matched,

            missing=missing,

            extra=extra,

            related=sorted(
                related,
            ),

            score=score,

        )