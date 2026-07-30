from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.planner.keyword_plan import (
    KeywordPlan,
)
from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)
from app.engine.models.planner.section_plan import (
    SectionPlan,
)


@dataclass(slots=True)
class OptimizationPlan:
    """
    Final execution plan produced by the Planner.

    This object defines WHAT changes should happen.

    It does NOT:
        - modify DOCX
        - generate text
        - call AI

    Responsibilities:

        Intelligence
             ↓
          Planner
             ↓
       OptimizationPlan
             ↓
          Optimizer
             ↓
           Writer
    """

    # --------------------------------------------------
    # Section Planning
    # --------------------------------------------------

    sections: list[SectionPlan] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Rewrite Instructions
    # --------------------------------------------------

    rewrites: list[RewritePlan] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Keyword Strategy
    # --------------------------------------------------

    keywords: KeywordPlan | None = None

    # --------------------------------------------------
    # Quality
    # --------------------------------------------------

    confidence: float = 0.0

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    warnings: list[str] = field(
        default_factory=list,
    )

    notes: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @property
    def rewrite_count(
        self,
    ) -> int:

        return len(
            self.rewrites
        )

    @property
    def section_count(
        self,
    ) -> int:

        return len(
            self.sections
        )

    def has_changes(
        self,
    ) -> bool:

        return bool(
            self.sections
            or self.rewrites
            or (
                self.keywords
                and self.keywords.keywords
            )
        )

    def add_warning(
        self,
        warning: str,
    ) -> None:

        self.warnings.append(
            warning
        )