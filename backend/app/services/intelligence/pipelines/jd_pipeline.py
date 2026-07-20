from app.services.intelligence.models import (
    JDAnalysis,
)

from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)

from app.services.intelligence.detectors.skill_classifier import (
    SkillClassifier,
)

from app.services.intelligence.detectors.jd_role_detector import (
    JDRoleDetector,
)

from app.services.intelligence.detectors.duplicate_detector import (
    DuplicateDetector,
)


class JDPipeline:
    """
    Builds JD Knowledge from a Job Description.
    """

    @classmethod
    def run(
        cls,
        job_description: str,
    ) -> JDAnalysis:

        # -------------------------------------
        # Detect Technologies
        # -------------------------------------

        technologies = TechnologyDetector.detect(
            job_description
        )

        # -------------------------------------
        # Convert to Skills
        # -------------------------------------

        skills = [

            SkillClassifier.classify(

                technology,

                source="jd",

            )

            for technology in technologies

        ]

        # -------------------------------------
        # Remove Duplicates
        # -------------------------------------

        skills = DuplicateDetector.remove_duplicate_skills(
            skills
        )

        # -------------------------------------
        # Detect Target Role
        # -------------------------------------

        target_role = JDRoleDetector.detect(
        skills
        )

        # -------------------------------------
        # Build JD Knowledge
        # -------------------------------------

        return JDAnalysis(

            target_role=target_role,

            skills=skills,

            original_text=job_description,

        )