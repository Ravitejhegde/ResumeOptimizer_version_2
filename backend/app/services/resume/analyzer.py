from app.schemas.resume_analysis import ResumeAnalysisResponse

from .extractor import ResumeExtractor
from .skill_extractor import ResumeSkillExtractor


class ResumeAnalyzer:

    @staticmethod
    def analyze(path: str):

        text = ResumeExtractor.extract(path)

        skills = ResumeSkillExtractor.extract(text)

        return ResumeAnalysisResponse(
            text=text,
            skills=skills,
        )