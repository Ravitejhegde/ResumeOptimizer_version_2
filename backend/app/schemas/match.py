from __future__ import annotations

from pydantic import BaseModel, Field


class MatchResponse(BaseModel):
    """
    Response containing resume and job description skill comparison.

    Contains:
        - ATS matching score
        - Matched skills
        - Missing skills
        - Additional detected skills
    """


    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Skill match score percentage",
    )


    matched_skills: list[str] = Field(
        default_factory=list,
        description="Skills found in both resume and job description",
    )


    missing_skills: list[str] = Field(
        default_factory=list,
        description="Required skills missing from resume",
    )


    extra_skills: list[str] = Field(
        default_factory=list,
        description="Additional skills found in resume",
    )