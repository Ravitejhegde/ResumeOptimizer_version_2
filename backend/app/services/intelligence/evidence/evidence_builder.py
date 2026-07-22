from app.services.intelligence.evidence.title_evidence import (
    TitleEvidence,
)

from app.services.intelligence.evidence.summary_evidence import (
    SummaryEvidence,
)

from app.services.intelligence.evidence.skills_evidence import (
    SkillsEvidence,
)

from app.services.intelligence.evidence.experience_evidence import (
    ExperienceEvidence,
)

from app.services.intelligence.evidence.projects_evidence import (
    ProjectsEvidence,
)

from app.services.intelligence.evidence.evidence_optimizer import (
    EvidenceOptimizer,
)


class EvidenceBuilder:
    """
    Builds normalized evidence from ResumeKnowledge.
    """

    @classmethod
    def build(
        cls,
        knowledge,
    ):

        evidence = []

        # -------------------------------------
        # Resume Title
        # -------------------------------------

        evidence.extend(

            TitleEvidence.build(
                knowledge.detected_role
            )

        )

        # -------------------------------------
        # Resume Summary
        # -------------------------------------

        evidence.extend(

            SummaryEvidence.build(
                knowledge.summary,
                knowledge.technologies,
            )

        )

        # -------------------------------------
        # Skills
        # -------------------------------------

        evidence.extend(

            SkillsEvidence.build(
                knowledge.technologies
            )

        )

        # -------------------------------------
        # Experience
        # -------------------------------------

        evidence.extend(

            ExperienceEvidence.build(
                knowledge.experience
            )

        )

        # -------------------------------------
        # Projects
        # -------------------------------------

        evidence.extend(

            ProjectsEvidence.build(
                knowledge.projects
            )

        )

        # -------------------------------------
        # Optimize Evidence
        # -------------------------------------

        return EvidenceOptimizer.optimize(
            evidence
        )