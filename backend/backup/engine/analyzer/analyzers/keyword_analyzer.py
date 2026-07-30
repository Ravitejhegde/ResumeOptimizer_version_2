from __future__ import annotations

from app.engine.analyzer.extractors.resume_skill_extractor import (
    ResumeSkillExtractor,
)
from app.engine.models.analysis.keyword_analysis import (
    KeywordAnalysis,
)
from app.engine.models.document.document import (
    Document,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class KeywordAnalyzer:
    """
    Performs keyword analysis.

    Responsibilities
    ----------------
    • Extract resume skills
    • Normalize skills
    • Categorize skills
    • Detect duplicates
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

        self._extractor = ResumeSkillExtractor(
            knowledge,
        )

    # --------------------------------------------------

    def analyze(
        self,
        document: Document,
    ) -> KeywordAnalysis:

        detected = self._extractor.extract(
            document,
        )

        normalized = (
            self._knowledge.normalize_many(
                detected,
            )
        )

        categories = (
            self._knowledge.categorize(
                normalized,
            )
        )

        duplicates = sorted(
            {
                skill
                for skill in normalized
                if normalized.count(skill) > 1
            }
        )

        return KeywordAnalysis(

            detected=detected,

            normalized=sorted(
                set(normalized),
            ),

            duplicates=duplicates,

            categories=categories,

        )
