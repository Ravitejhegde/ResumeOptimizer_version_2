from __future__ import annotations

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)
from app.knowledge.services.technology_extractor import (
    TechnologyExtractor,
)
from app.engine.models.jd_analysis import (
    JDAnalysis,
)


class JobDescriptionAnalyzer:
    """
    Analyzes a Job Description.

    Responsibilities
    ----------------
    • Extract technologies
    • Normalize technologies
    • Produce a structured JDAnalysis

    Future Responsibilities
    -----------------------
    • Detect role
    • Detect seniority
    • Detect experience
    • Detect responsibilities
    • Detect preferred skills
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._extractor = TechnologyExtractor(
            taxonomy=knowledge.taxonomy,
            normalizer=knowledge.normalizer,
        )

    def analyze(
        self,
        text: str,
    ) -> JDAnalysis:

        skills = self._extractor.extract(
            text
        )

        return JDAnalysis(

            required_skills=skills,

            preferred_skills=[],

            keywords=skills,

        )




