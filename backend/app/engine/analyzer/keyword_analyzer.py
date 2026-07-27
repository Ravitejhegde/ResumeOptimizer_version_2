from __future__ import annotations

from app.engine.models.analysis_result import (
    KeywordAnalysisResult,
)
from app.engine.models.document import (
    Document,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class KeywordAnalyzer:
    """
    Extracts technologies from a resume.

    Responsibilities
    ----------------
    • Detect technologies
    • Normalize technologies
    • Remove duplicates
    • Categorize technologies
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    def analyze(
        self,
        document: Document,
    ) -> KeywordAnalysisResult:

        detected: list[str] = []

        for paragraph in document.paragraphs:

            detected.extend(
                self._knowledge.extract(
                    paragraph.text
                )
            )

        normalized = sorted(
            set(detected)
        )

        categorized = {}

        duplicates = []

        return KeywordAnalysisResult(
            detected_skills=normalized,
            normalized_skills=normalized,
            categorized_skills=categorized,
            duplicate_skills=duplicates,
        )



