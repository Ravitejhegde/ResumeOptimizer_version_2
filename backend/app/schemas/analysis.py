from pydantic import BaseModel, Field


class ResumeAnalysisRequest(BaseModel):
    """
    Request payload for resume analysis.
    """

    resume_id: str = Field(
        ...,
        min_length=1,
        description="Uploaded resume ID",
    )

    job_description: str = Field(
        ...,
        min_length=1,
        description="Target job description",
    )




