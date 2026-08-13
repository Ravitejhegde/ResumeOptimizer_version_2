"""
app.planner.prompt.prompt_plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents prompts generated for the AI optimizer.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptPlan:
    """
    Collection of prompts prepared for AI execution.
    """

    prompts: list[str] = field(
        default_factory=list
    )

    estimated_tokens: int = 0

    prompt_count: int = 0