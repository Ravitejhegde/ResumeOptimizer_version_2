from app.models.resume_profile import ResumeProfile

from .skill_extractor import ResumeSkillExtractor
from .experience_extractor import ExperienceExtractor
from .education_extractor import EducationExtractor
from .project_extractor import ProjectExtractor


class ResumeProfileBuilder:

    @staticmethod
    def build(text: str) -> ResumeProfile:

        profile = ResumeProfile()

        profile.skills = ResumeSkillExtractor.extract(text)

        profile.experience = ExperienceExtractor.extract(text)

        profile.education = EducationExtractor.extract(text)

        profile.projects = ProjectExtractor.extract(text)

        return profile