from __future__ import annotations

import re

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.analysis_result import (
    KeywordAnalysisResult,
)
from app.engine.models.document import (
    Document,
)


class KeywordAnalyzer:
    """
    Extracts and understands technologies found
    in a resume.

    Responsibilities
    ----------------
    - Extract keywords
    - Normalize technologies
    - Remove duplicates
    - Categorize skills

    Never modifies the document.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._knowledge = knowledge

    def analyze(
        self,
        document: Document,
    ) -> KeywordAnalysisResult:

        extracted: list[str] = []

        for paragraph in document.paragraphs:

            words = re.findall(
                r"[A-Za-z0-9.+#-]+",
                paragraph.text,
            )

            extracted.extend(words)

        normalized = self._knowledge.normalizer.normalize_many(
            extracted
        )

        unique_skills = sorted(
            set(normalized)
        )

        duplicates = sorted(
            {
                skill
                for skill in normalized
                if normalized.count(skill) > 1
            }
        )

        categorized = (
            self._knowledge.categorizer.categorize(
                unique_skills
            )
        )

        return KeywordAnalysisResult(
            detected_skills=sorted(set(extracted)),
            normalized_skills=unique_skills,
            categorized_skills=categorized,
            duplicate_skills=duplicates,
        )