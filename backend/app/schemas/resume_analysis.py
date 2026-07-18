from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    text: str
    skills: list[str]