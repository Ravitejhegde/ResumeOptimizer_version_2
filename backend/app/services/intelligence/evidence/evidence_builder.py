from app.services.intelligence.evidence.title_evidence import TitleEvidence
from app.services.intelligence.evidence.summary_evidence import SummaryEvidence
from app.services.intelligence.evidence.skills_evidence import SkillsEvidence
from app.services.intelligence.evidence.experience_evidence import ExperienceEvidence
from app.services.intelligence.evidence.projects_evidence import ProjectsEvidence


class EvidenceBuilder:

    @classmethod
    def build(
        cls,
        resume,
    ):

        evidence = []

        evidence.extend(
            TitleEvidence.build(
                resume.detected_role
            )
        )

        evidence.extend(
            SummaryEvidence.build(
                resume.summary
            )
        )

        evidence.extend(
            SkillsEvidence.build(
                resume.skills
            )
        )

        evidence.extend(
            ExperienceEvidence.build(
                resume.experience
            )
        )

        evidence.extend(
            ProjectsEvidence.build(
                resume.projects
            )
        )

        return evidence