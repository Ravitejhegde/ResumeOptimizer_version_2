from __future__ import annotations

from app.engine.analyzer.resume_skill_extractor import (
    ResumeSkillExtractor,
)
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
    Analyzes resume technologies.

    Responsibilities
    ----------------
    • Normalize detected skills
    • Remove duplicates
    • Categorize skills

    Never reads document text directly.
    Never extracts technologies.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

        self._extractor = ResumeSkillExtractor(
            knowledge,
        )

    def analyze(
        self,
        document: Document,
    ) -> KeywordAnalysisResult:

        detected = self._extractor.extract(
            document,
        )

        normalized = (
            self._knowledge.normalize_many(
                detected,
            )
        )

        duplicates = sorted(
            {
                skill
                for skill in normalized
                if normalized.count(skill) > 1
            }
        )

        categorized = (
            self._knowledge.categorize(
                normalized,
            )
        )

        unique = sorted(
            set(normalized),
        )

        return KeywordAnalysisResult(
            detected_skills=detected,
            normalized_skills=unique,
            categorized_skills=categorized,
            duplicate_skills=duplicates,
        )