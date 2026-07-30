from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.ai.prompt_context import (
    PromptContext,
)


@dataclass(slots=True)
class PromptRequest:
    """
    Structured request sent to an AI provider.

    AI services consume this model.
    """

    context: PromptContext

    task: str = "rewrite_resume"

    model: str | None = None

    temperature: float = 0.2

    metadata: dict[str, str] = field(
        default_factory=dict,
    )