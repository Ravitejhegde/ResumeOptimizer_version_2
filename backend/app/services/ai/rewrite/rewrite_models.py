from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewriteRequest:
    """
    Represents one paragraph rewrite request.
    """

    paragraph: str

    target_role: str

    selected_skills: list[str]

    max_words: int


@dataclass(slots=True)
class RewriteResult:
    """
    Result returned by an AI provider.
    """

    optimized_text: str

    success: bool

    provider: str

    tokens_used: int = 0




