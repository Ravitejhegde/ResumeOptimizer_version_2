from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KeywordDecision:
    """
    One keyword optimization decision.

    Represents a keyword that should be
    introduced, improved, or preserved.
    """

    keyword: str

    category: str | None = None

    action: str = "add"

    priority: int = 0

    reason: str = ""

    confidence: float = 0.0


@dataclass(slots=True)
class KeywordPlan:
    """
    Keyword optimization plan produced
    by the Planner.

    Responsibilities:

    - Select important keywords
    - Prioritize keywords
    - Explain decisions

    Does NOT modify documents.
    """

    keywords: list[KeywordDecision] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    def add(
        self,
        keyword: KeywordDecision,
    ) -> None:

        self.keywords.append(
            keyword
        )

    def high_priority(
        self,
    ) -> list[KeywordDecision]:

        return [
            item
            for item in self.keywords
            if item.priority <= 1
        ]