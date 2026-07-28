from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)


@dataclass(slots=True)
class OptimizationRequest:
    """
    Input to the Optimizer.
    """

    document: Document

    plan: OptimizationPlan
