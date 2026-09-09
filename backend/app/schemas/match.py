from __future__ import annotations

from pydantic import BaseModel, Field


class MatchResponse(BaseModel):
    """
    Response containing resume and job description
    skill and technology comparison.

    Contains:
        - ATS matching score
        - Detected canonical role ID
        - Matched skills
        - Missing skills
        - Matched technologies
        - Missing technologies
        - Additional detected skills
    """

    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Skill match score percentage",
    )

    role_id: str = Field(
        ...,
        min_length=1,
        description="Canonical detected role ID",
    )

    matched_skills: list[str] = Field(
        default_factory=list,
        description="Skills found in both resume and job description",
    )

    missing_skills: list[str] = Field(
        default_factory=list,
        description="Required skills missing from resume",
    )

    matched_technologies: list[str] = Field(
        default_factory=list,
        description="Technologies found in both resume and job description",
    )

    missing_technologies: list[str] = Field(
        default_factory=list,
        description="Required technologies missing from resume",
    )

    extra_skills: list[str] = Field(
        default_factory=list,
        description="Additional skills found in resume",
    )