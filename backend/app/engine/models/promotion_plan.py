from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromotionDecision:
    """
    One optimization decision.
    """

    skill: str

    category: str

    priority: int

    evidence_found: bool

    confidence: float

    action: str

    target_section: str | None = None

    reason: str = ""


@dataclass(slots=True)
class PromotionPlan:
    """
    Master promotion plan used by the optimizer.
    """

    decisions: list[PromotionDecision] = field(
        default_factory=list
    )