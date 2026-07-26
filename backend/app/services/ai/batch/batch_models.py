from __future__ import annotations

from pydantic import BaseModel, Field


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
    Entire resume rewrite request.
    """

    target_role: str

    selected_skills: list[str]

    locked: LockedEntities = Field(
        default_factory=LockedEntities
    )

    paragraphs: list[ParagraphRewriteRequest]


class ParagraphRewriteResult(BaseModel):
    """
    Rewritten paragraph returned by AI.
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