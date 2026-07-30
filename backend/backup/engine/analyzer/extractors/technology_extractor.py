from __future__ import annotations

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class TechnologyExtractor:
    """
    Extracts technologies using the
    Knowledge Platform.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    # --------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[str]:

        return self._knowledge.extract(
            text,
        )
