from __future__ import annotations

import re

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.document import Document


class KeywordAnalyzer:
    """
    Extracts normalized technologies and keywords
    from a resume.

    This analyzer never modifies the document.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._knowledge = knowledge

    def analyze(
        self,
        document: Document,
    ) -> list[str]:

        keywords: list[str] = []

        for paragraph in document.paragraphs:

            text = paragraph.text

            words = re.findall(

                r"[A-Za-z0-9.+#-]+",

                text,

            )

            keywords.extend(words)

        return self._knowledge.normalizer.normalize_many(
            keywords
        )