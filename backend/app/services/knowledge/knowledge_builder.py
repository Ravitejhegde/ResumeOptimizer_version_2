from app.services.knowledge.extractors.achievement_extractor import AchievementExtractor
from app.services.knowledge.extractors.certification_extractor import CertificationExtractor
from app.services.knowledge.extractors.education_extractor import EducationExtractor
from app.services.knowledge.extractors.email_extractor import EmailExtractor
from app.services.knowledge.extractors.experience_extractor import ExperienceExtractor
from app.services.knowledge.extractors.language_extractor import LanguageExtractor
from app.services.knowledge.extractors.name_extractor import NameExtractor
from app.services.knowledge.extractors.phone_extractor import PhoneExtractor
from app.services.knowledge.extractors.project_extractor import ProjectExtractor
from app.services.knowledge.extractors.skills_extractor import SkillsExtractor
from app.services.knowledge.extractors.technology_extractor import TechnologyExtractor
from app.services.knowledge.models import ResumeKnowledge
from app.services.knowledge.section_detector import SectionDetector
from app.services.parser.models import ResumeDocument


class KnowledgeBuilder:
    """
    Builds structured knowledge from a parsed resume.
    """

    @staticmethod
    def build(
        document: ResumeDocument,
    ) -> ResumeKnowledge:

        sections = SectionDetector.detect(
            document,
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        knowledge = ResumeKnowledge()

        knowledge.sections = sections

        knowledge.total_sections = len(
            sections,
        )

        knowledge.detected_name = NameExtractor.extract(
            document,
        )

        knowledge.detected_email = EmailExtractor.extract(
            text,
        )

        knowledge.detected_phone = PhoneExtractor.extract(
            text,
        )

        knowledge.skills = SkillsExtractor.extract(
            sections,
        )

        knowledge.technologies = TechnologyExtractor.extract(
            sections,
        )

        knowledge.education = EducationExtractor.extract(
            sections,
        )

        knowledge.experience = ExperienceExtractor.extract(
            sections,
        )

        knowledge.projects = ProjectExtractor.extract(
            sections,
        )

        knowledge.certifications = CertificationExtractor.extract(
            sections,
        )

        knowledge.languages = LanguageExtractor.extract(
            sections,
        )

        knowledge.achievements = AchievementExtractor.extract(
            sections,
        )

        knowledge.total_skills = len(
            knowledge.skills,
        )

        knowledge.total_projects = len(
            knowledge.projects,
        )

        knowledge.total_experience = len(
            knowledge.experience,
        )

        knowledge.total_education = len(
            knowledge.education,
        )

        knowledge.has_summary = (
            knowledge.summary != ""
        )

        knowledge.has_projects = (
            len(knowledge.projects) > 0
        )

        knowledge.has_certifications = (
            len(knowledge.certifications) > 0
        )

        return knowledge