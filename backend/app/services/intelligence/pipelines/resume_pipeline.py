from app.services.intelligence.models import (
    ResumeAnalysis,
)

from app.services.intelligence.detectors.section_detector import (
    SectionDetector,
)

from app.services.intelligence.detectors.block_indexer import (
    BlockIndexer,
)

from app.services.intelligence.detectors.technology_map_builder import (
    TechnologyMapBuilder,
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

from app.services.intelligence.detectors.hyperlink_detector import (
    HyperlinkDetector,
)

from app.services.intelligence.detectors.role_detector import (
    RoleDetector,
)

from app.services.intelligence.detectors.skill_classifier import (
    SkillClassifier,
)

from app.services.intelligence.detectors.confidence_calculator import (
    ConfidenceCalculator,
)

from app.services.intelligence.detectors.duplicate_detector import (
    DuplicateDetector,
)


class ResumePipeline:
    """
    Builds Resume Knowledge from document blocks.
    """

    @classmethod
    def run(
        cls,
        blocks,
    ) -> ResumeAnalysis:

        # -------------------------------------
        # Detect Resume Sections
        # -------------------------------------

        detected_sections = SectionDetector.detect(
            blocks
        )

        indexed_sections = BlockIndexer.build(
            detected_sections
        )

        # -------------------------------------
        # Detect Technologies
        # -------------------------------------

        technology_map = TechnologyMapBuilder.build(
            blocks
        )

        # -------------------------------------
        # Resume Components
        # -------------------------------------

        summary = SummaryDetector.detect(
            indexed_sections.get(
                "SUMMARY",
                []
            )
        )

        experience = ExperienceDetector.detect(
            indexed_sections.get(
                "EXPERIENCE",
                []
            )
        )

        projects = ProjectDetector.detect(
            indexed_sections.get(
                "PROJECTS",
                []
            )
        )

        education = EducationDetector.detect(
            indexed_sections.get(
                "EDUCATION",
                []
            )
        )

        hyperlinks = HyperlinkDetector.detect(
            blocks
        )

        # -------------------------------------
        # Build Skills
        # -------------------------------------

        skills = []

        for technologies in technology_map.values():

            for technology in technologies:

                skills.append(

                    SkillClassifier.classify(

                        technology,

                        source="resume",

                    )

                )

        # -------------------------------------
        # Confidence
        # -------------------------------------

        skills = ConfidenceCalculator.calculate(
            skills
        )

        # -------------------------------------
        # Remove Duplicates
        # -------------------------------------

        skills = DuplicateDetector.remove_duplicate_skills(
            skills
        )

        # -------------------------------------
        # Build Resume
        # -------------------------------------

        resume = ResumeAnalysis(

            detected_role="Unknown",

            skills=skills,

            technologies=skills,

            sections=list(
                indexed_sections.keys()
            ),

            summary=summary,

            experience=experience,

            projects=projects,

            education=education,

            hyperlinks=hyperlinks,

            total_skill_capacity=len(
                skills
            ),

        )

        # -------------------------------------
        # Detect Role using Evidence Engine
        # -------------------------------------

        resume.detected_role = RoleDetector.detect(
            resume
        )

        return resume