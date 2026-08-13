"""
app.ai.models.ai_response
~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized response returned by an AI provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AIResponse:
    """
    Standard response produced by any AI provider.
    """

    content: str = ""

    model: str = ""

    provider: str = ""

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    finish_reason: str = ""

    success: bool = False

    error: str = ""

    metadata: dict[str, str] = field(
        default_factory=dict,
    )