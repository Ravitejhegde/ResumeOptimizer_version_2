from __future__ import annotations

from pydantic import BaseModel, Field


class JobAnalysisResponse(BaseModel):
    """
    Response returned after analyzing a job description.

    Contains:
        - Detected role/title
        - Experience requirement
        - Extracted skills
    """


    title: str = Field(
        ...,
        description="Detected job title or role",
    )


    experience: str | None = Field(
        default=None,
        description="Required experience level",
    )


    skills: list[str] = Field(
        default_factory=list,
        description="Extracted technical and domain skills",
    )