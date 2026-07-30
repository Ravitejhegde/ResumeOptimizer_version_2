from __future__ import annotations

import re

from app.engine.models.analysis.jd_analysis import (
    JDAnalysis,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class JobDescriptionAnalyzer:
    """
    Analyzes a Job Description using the
    Knowledge Platform.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    # --------------------------------------------------

    def analyze(
        self,
        text: str,
    ) -> JDAnalysis:

        # Extract technologies from the JD
        detected = self._knowledge.extract(
            text,
        )

        # Normalize technology names
        normalized = self._knowledge.normalize_many(
            detected,
        )

        # TODO:
        # Re-implement role detection using the new
        # KnowledgeManager API.
        role = None

        return JDAnalysis(

            role=role,

            required_skills=normalized,

            preferred_skills=[],

            keywords=normalized,

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