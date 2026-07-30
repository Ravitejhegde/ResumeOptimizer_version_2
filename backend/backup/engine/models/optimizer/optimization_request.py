from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)


@dataclass(slots=True)
class OptimizationRequest:
    """
    Input provided to the Optimizer.

    Contains:

        Document
            +
        Optimization Plan

    The Optimizer decides HOW to apply
    the planned changes.
    """

    document: Document

    plan: OptimizationPlan

    request_id: str | None = None

    preserve_formatting: bool = True

    metadata: dict[str, str] = field(
        default_factory=dict,
    )