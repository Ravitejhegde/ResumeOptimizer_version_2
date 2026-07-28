from __future__ import annotations

import re

from app.engine.models.jd_analysis import (
    JDAnalysis,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class JobDescriptionAnalyzer:
    """
    Analyze a Job Description.

    Responsibilities
    ----------------
    • Extract technologies
    • Normalize technologies
    • Detect experience
    • Produce JDAnalysis

    Future
    ------
    • Role detection
    • Seniority detection
    • Responsibilities
    • Qualifications
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    def analyze(
        self,
        text: str,
    ) -> JDAnalysis:

        detected = self._knowledge.extract(
            text,
        )

        skills = self._knowledge.normalize_many(
            detected,
        )

        return JDAnalysis(

            required_skills=skills,

            preferred_skills=[],

            keywords=skills,

            minimum_experience=self._detect_experience(
                text,
            ),
        )

    # --------------------------------------------------

    @staticmethod
    def _detect_experience(
        text: str,
    ) -> float | None:

        match = re.search(
            r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
            text,
            re.IGNORECASE,
        )

        if match is None:
            return None

        return float(
            match.group(1),
        )