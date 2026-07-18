from pydantic import BaseModel
from typing import List


class ResumeSection(BaseModel):
    title: str
    content: str


class ParsedResume(BaseModel):
    sections: List[ResumeSection]