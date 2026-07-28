from __future__ import annotations

from app.engine.models.document import Document
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class ResumeSkillExtractor:
    """
    Extract technologies from a resume.

    Responsibilities
    ----------------
    • Read document text
    • Detect technologies
    • Return detected skills

    Never normalizes.
    Never categorizes.
    Never scores.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    def extract(
        self,
        document: Document,
    ) -> list[str]:

        skills: list[str] = []

        for paragraph in document.paragraphs:

            skills.extend(
                self._knowledge.extract(
                    paragraph.text
                )
            )

        return skills