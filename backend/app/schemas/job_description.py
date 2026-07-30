from __future__ import annotations

from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """
    Request payload for analyzing a job description.
    """


    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description text",
    )