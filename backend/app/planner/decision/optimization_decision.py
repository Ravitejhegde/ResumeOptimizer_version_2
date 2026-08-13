"""
app.planner.decision.optimization_decision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the planner's optimization decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationDecision:
    """
    High-level decision produced by the planner.
    """

    should_optimize: bool = True

    optimization_level: str = "moderate"

    strategy: str = ""

    reason: str = ""

    warnings: list[str] = field(
        default_factory=list
    )