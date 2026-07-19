from app.services.intelligence.models import (
    ResumeAnalysis,
)

from app.services.intelligence.detectors.section_detector import (
    SectionDetector,
)

from app.services.intelligence.detectors.block_indexer import (
    BlockIndexer,
)

from app.services.intelligence.detectors.summary_detector import (
    SummaryDetector,
)

from app.services.intelligence.detectors.experience_detector import (
    ExperienceDetector,
)

from app.services.intelligence.detectors.project_detector import (
    ProjectDetector,
)

from app.services.intelligence.detectors.education_detector import (
    EducationDetector,
)

from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)

from app.services.intelligence.detectors.skill_classifier import (
    SkillClassifier,
)

from app.services.intelligence.detectors.role_detector import (
    RoleDetector,
)

from app.services.intelligence.detectors.confidence_calculator import (
    ConfidenceCalculator,
)

from app.services.intelligence.detectors.duplicate_detector import (
    DuplicateDetector,
)

from app.services.intelligence.detectors.hyperlink_detector import (
    HyperlinkDetector,
)


class ResumeAnalyzer:
    """
    Main Resume Analyzer.

    Orchestrates all resume detectors and
    returns a ResumeAnalysis object.
    """

    @classmethod
    def analyze(
        cls,
        blocks,
    ) -> ResumeAnalysis:

        # ---------------------------------
        # Detect Sections
        # ---------------------------------

        detected_sections = SectionDetector.detect(
            blocks
        )

        indexed_sections = BlockIndexer.build(
            detected_sections
        )

        # ---------------------------------
        # Detect Resume Parts
        # ---------------------------------

        summary = SummaryDetector.detect(
            indexed_sections.get(
                "SUMMARY",
                [],
            )
        )

        experience = ExperienceDetector.detect(
            indexed_sections.get(
                "EXPERIENCE",
                [],
            )
        )

        projects = ProjectDetector.detect(
            indexed_sections.get(
                "PROJECTS",
                [],
            )
        )

        education = EducationDetector.detect(
            indexed_sections.get(
                "EDUCATION",
                [],
            )
        )

        hyperlinks = HyperlinkDetector.detect(
            blocks
        )

        # ---------------------------------
        # Detect Technologies
        # ---------------------------------

        detected = TechnologyDetector.detect(

            "\n".join(

                block.text

                for block in blocks

            )

        )

        skills = [

            SkillClassifier.classify(

                technology,

                source="resume",

            )

            for technology in detected

        ]

        # ---------------------------------
        # Confidence
        # ---------------------------------

        skills = ConfidenceCalculator.calculate(
            skills
        )

        # ---------------------------------
        # Remove Duplicates
        # ---------------------------------

        skills = DuplicateDetector.remove_duplicate_skills(
            skills
        )

        # ---------------------------------
        # Detect Role
        # ---------------------------------

        detected_role = RoleDetector.detect(
            skills
        )

        # ---------------------------------
        # Capacity
        # ---------------------------------

        total_skill_capacity = len(
            skills
        )

        # ---------------------------------
        # Build Analysis
        # ---------------------------------

        return ResumeAnalysis(

            detected_role=detected_role,

            skills=skills,

            sections=list(
                indexed_sections.keys()
            ),

            summary=summary,

            experience=experience,

            projects=projects,

            education=education,

            hyperlinks=hyperlinks,

            total_skill_capacity=total_skill_capacity,

        )