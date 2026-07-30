from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewriteRequest:
    """
    Legacy single paragraph rewrite request.

    Deprecated:
        Use BatchRewriteRequest from
        app.engine.models.ai instead.
    """

    paragraph_id: str

    paragraph: str

    section: str = ""

    target_role: str = ""

    selected_skills: list[str] | None = None

    max_words: int = 0

    max_characters: int = 0


@dataclass(slots=True)
class RewriteResult:
    """
    Legacy single rewrite result.

    Deprecated:
        Use BatchRewriteResult instead.
    """

    paragraph_id: str

    optimized_text: str

    success: bool

    provider: str

    tokens_used: int = 0

    error: str | None = None