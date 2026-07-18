from pydantic import BaseModel


class MatchResponse(BaseModel):

    score: int

    matched_skills: list[str]

    missing_skills: list[str]

    extra_skills: list[str]