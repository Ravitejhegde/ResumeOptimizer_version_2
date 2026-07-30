from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeAnalysisRequest(BaseModel):
    """
    Request payload for resume analysis.

    Supports:
        - Resume-only analysis
        - Resume + Job Description comparison
    """


    resume_id: str = Field(
        ...,
        min_length=1,
        description="Uploaded resume ID",
    )


    job_description: str | None = Field(
        default=None,
        min_length=10,
        description=(
            "Optional target job description "
            "for ATS comparison"
        ),
    )