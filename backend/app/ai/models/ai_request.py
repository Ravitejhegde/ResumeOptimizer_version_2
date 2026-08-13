"""
app.ai.models.ai_request
~~~~~~~~~~~~~~~~~~~~~~~~

Represents an AI generation request.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AIRequest:
    """
    Standard request sent to an AI provider.
    """

    prompt: str

    system_prompt: str = ""

    model: str = ""

    temperature: float = 0.3

    max_tokens: int = 4096

    metadata: dict[str, str] = field(
        default_factory=dict,
    )