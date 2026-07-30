from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptResponse:
    """
    Structured response returned by AI provider.

    Contains generated content and
    explainability information.
    """

    content: str

    success: bool = True

    model: str | None = None

    confidence: float = 0.0

    tokens_used: int | None = None

    warnings: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, str] = field(
        default_factory=dict,
    )