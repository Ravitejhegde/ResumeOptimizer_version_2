"""
app.planner.section.section_plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents where optimization should occur.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionPlan:
    """
    Planning information for resume sections.
    """

    sections: dict[str, list[str]] = field(
    default_factory=dict
)

    paragraph_ids: dict[str, list[str]] = field(
    default_factory=dict
)

    untouched_sections: list[str] = field(
        default_factory=list
    )

    reasoning: dict[str, str] = field(
        default_factory=dict
    )