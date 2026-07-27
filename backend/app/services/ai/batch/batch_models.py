from __future__ import annotations

from pydantic import BaseModel, Field

from app.engine.models.optimization_strategy import (
    OptimizationStrategy,
)


class LockedEntities(BaseModel):
    """
    Values that the AI must never modify.
    """

    companies: list[str] = Field(default_factory=list)

    dates: list[str] = Field(default_factory=list)

    degrees: list[str] = Field(default_factory=list)

    colleges: list[str] = Field(default_factory=list)

    project_names: list[str] = Field(default_factory=list)

    locations: list[str] = Field(default_factory=list)


class ParagraphRewriteRequest(BaseModel):
    """
    A single paragraph to rewrite.
    """

    id: str

    type: str

    text: str

    max_characters: int

    max_words: int

    rewrite: bool = True


class BatchRewriteRequest(BaseModel):
    """
    Complete resume rewrite request.

    This is the only object passed to
    the Prompt Builder.
    """

    # ----------------------------------
    # Intelligence
    # ----------------------------------

    optimization_strategy: (
        OptimizationStrategy | None
    ) = None

    target_role: str = ""

    selected_skills: list[str] = Field(
        default_factory=list
    )

    # ----------------------------------
    # Locked Content
    # ----------------------------------

    locked: LockedEntities = Field(
        default_factory=LockedEntities
    )

    # ----------------------------------
    # Paragraphs
    # ----------------------------------

    paragraphs: list[
        ParagraphRewriteRequest
    ] = Field(default_factory=list)


class ParagraphRewriteResult(BaseModel):
    """
    AI rewritten paragraph.
    """

    id: str

    text: str


class BatchRewriteResult(BaseModel):
    """
    Parsed AI response.
    """

    paragraphs: list[
        ParagraphRewriteResult
    ] = Field(default_factory=list)

    success: bool

    provider: str




