from pydantic import BaseModel


class JobAnalysisResponse(BaseModel):

    title: str

    experience: str

    skills: list[str]