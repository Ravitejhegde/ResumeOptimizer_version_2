from __future__ import annotations

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.knowledge.technology_extractor import (
    TechnologyExtractor,
)
from app.engine.models.analysis_result import (
    KeywordAnalysisResult,
)
from app.engine.models.document import (
    Document,
)


class KeywordAnalyzer:
    """
    Extracts technologies from the resume.

    Responsibilities
    ----------------
    • Detect technologies
    • Normalize technologies
    • Remove duplicates
    • Categorize technologies

    Never extracts arbitrary words.
    Never modifies the document.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._knowledge = knowledge

        self._extractor = TechnologyExtractor(
            taxonomy=knowledge.taxonomy,
            normalizer=knowledge.normalizer,
        )

    def analyze(
        self,
        document: Document,
    ) -> KeywordAnalysisResult:

        detected: list[str] = []

        # -----------------------------------------
        # Extract technologies
        # -----------------------------------------

        for paragraph in document.paragraphs:

            detected.extend(
                self._extractor.extract(
                    paragraph.text
                )
            )

        # -----------------------------------------
        # Normalize
        # -----------------------------------------

        normalized = (
            self._knowledge.normalizer.normalize_many(
                detected
            )
        )

        unique = sorted(
            set(normalized)
        )

        # -----------------------------------------
        # Duplicate technologies
        # -----------------------------------------

        duplicates = sorted(
            {
                skill
                for skill in normalized
                if normalized.count(skill) > 1
            }
        )

        # -----------------------------------------
        # Categorize
        # -----------------------------------------

        categorized = (
            self._knowledge.categorizer.categorize(
                unique
            )
        )

        return KeywordAnalysisResult(

            detected_skills=unique,

            normalized_skills=unique,

            categorized_skills=categorized,

            duplicate_skills=duplicates,

        )