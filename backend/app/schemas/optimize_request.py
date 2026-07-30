from __future__ import annotations

from pydantic import BaseModel, Field


class OptimizeRequest(BaseModel):
    """
    Request payload for resume optimization.

    Contains:
        - Resume to optimize
        - Target job description
        - Selected technologies to promote
    """


    resume_id: str = Field(
        ...,
        min_length=1,
        description="Uploaded resume ID",
    )


    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )


    selected_skills: list[str] = Field(
        default_factory=list,
        description="Skills selected for optimization",
    )