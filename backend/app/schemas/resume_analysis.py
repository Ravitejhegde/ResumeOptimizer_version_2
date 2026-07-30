from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeAnalysisResponse(BaseModel):
    """
    Response returned after resume analysis.

    Contains:
        - Extracted resume information
        - Detected skills
        - ATS comparison results
    """


    text: str = Field(
        ...,
        description="Extracted resume text",
    )


    skills: list[str] = Field(
        default_factory=list,
        description="Detected resume skills",
    )


    score: int | None = Field(
        default=None,
        ge=0,
        le=100,
        description="ATS compatibility score",
    )


    matched_skills: list[str] = Field(
        default_factory=list,
        description="Skills matching job requirements",
    )


    missing_skills: list[str] = Field(
        default_factory=list,
        description="Required missing skills",
    )


    extra_skills: list[str] = Field(
        default_factory=list,
        description="Additional resume skills",
    )


    detected_role: str | None = Field(
        default=None,
        description="Detected target role",
    )


    experience: str | None = Field(
        default=None,
        description="Detected experience requirement",
    )