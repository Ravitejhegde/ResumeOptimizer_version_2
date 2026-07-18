from pydantic import BaseModel


class ResumeAnalysisRequest(BaseModel):

    resume_id: str

    job_description: str