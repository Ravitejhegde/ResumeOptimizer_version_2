"""
app.planner.rewrite.rewrite_plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines how each resume section should be rewritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RewritePlan:
    """
    Rewrite strategy for the optimization process.
    """

    section_levels: dict[str, str] = field(
        default_factory=dict
    )

    section_actions: dict[str, list[str]] = field(
        default_factory=dict
    )

    global_strategy: str = "moderate"

    reasoning: dict[str, str] = field(
        default_factory=dict
    )