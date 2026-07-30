from __future__ import annotations

from pydantic import BaseModel, Field


class LockedEntities(BaseModel):
    """
    Content that AI must never modify.

    These entities are protected during rewriting.
    """

    companies: list[str] = Field(
        default_factory=list,
    )

    dates: list[str] = Field(
        default_factory=list,
    )

    degrees: list[str] = Field(
        default_factory=list,
    )

    colleges: list[str] = Field(
        default_factory=list,
    )

    project_names: list[str] = Field(
        default_factory=list,
    )

    locations: list[str] = Field(
        default_factory=list,
    )


class ParagraphRewriteRequest(BaseModel):
    """
    Single paragraph rewrite instruction.
    """

    id: str

    paragraph_type: str

    text: str

    max_characters: int = 0

    max_words: int = 0

    rewrite: bool = True


class OptimizationContext(BaseModel):
    """
    Serializable intelligence context
    passed to AI.

    This avoids coupling AI models
    with engine dataclasses.
    """

    target_role: str = ""

    role_family: str = ""

    goals: list[str] = Field(
        default_factory=list,
    )

    selected_skills: list[str] = Field(
        default_factory=list,
    )


class BatchRewriteRequest(BaseModel):
    """
    Complete rewrite request.

    This is the input contract
    for PromptBuilder.
    """

    intelligence: OptimizationContext | None = None


    locked: LockedEntities = Field(
        default_factory=LockedEntities,
    )


    paragraphs: list[
        ParagraphRewriteRequest
    ] = Field(
        default_factory=list,
    )


class ParagraphRewriteResult(BaseModel):
    """
    Result of one AI rewrite.
    """

    id: str

    text: str


class BatchRewriteResult(BaseModel):
    """
    Parsed AI provider response.
    """

    paragraphs: list[
        ParagraphRewriteResult
    ] = Field(
        default_factory=list,
    )

    success: bool = True

    provider: str = ""