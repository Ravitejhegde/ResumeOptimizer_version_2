from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    resume_id: str
    job_description: str




