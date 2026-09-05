"""
Optimizer integration test.

Runs the complete optimization pipeline.

Resume
    ↓
Analyzer
    ↓
Understanding
    ↓
Job Understanding
    ↓
Gap Analysis
    ↓
Planner
    ↓
Optimizer
"""

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)
from app.analyzer.document.section_analyzer import (
    SectionAnalyzer,
)
from app.analyzer.experience.experience_analyzer import (
    ExperienceAnalyzer,
)
from app.analyzer.project.project_analyzer import (
    ProjectAnalyzer,
)
from app.analyzer.role.role_analyzer import (
    RoleAnalyzer,
)
from app.analyzer.skill.skill_analyzer import (
    SkillAnalyzer,
)
from app.analyzer.technology.technology_analyzer import (
    TechnologyAnalyzer,
)
from app.gap_analysis.services.gap_analyzer import (
    GapAnalyzer,
)
from app.job_description.services.job_description_parser import (
    JobDescriptionParser,
)
from app.job_understanding.services.job_understanding_builder import (
    JobUnderstandingBuilder,
)
from app.optimizer.services.optimizer import (
    Optimizer,
)
from app.planner.services.planner import (
    Planner,
)
from app.understanding.services.understanding_builder import (
    UnderstandingBuilder,
)

RESUME = (
    r"tests\resources\sample_resume.docx"
)

JOB_DESCRIPTION = """
Backend Developer

Requirements

Python
FastAPI
REST API
Authentication
Microservices
Docker
Redis
JWT
SQL
"""


def main() -> None:

    # -------------------------------------------------
    # Resume Analysis
    # -------------------------------------------------

    document = (
        DocumentAnalyzer().analyze(
            RESUME,
        )
    )

    document = (
        SectionAnalyzer().analyze(
            document,
        )
    )

    document = (
        TechnologyAnalyzer().analyze(
            document,
        )
    )

    document = (
        SkillAnalyzer().analyze(
            document,
        )
    )

    document = (
        RoleAnalyzer().analyze(
            document,
        )
    )

    document = (
        ExperienceAnalyzer().analyze(
            document,
        )
    )

    document = (
        ProjectAnalyzer().analyze(
            document,
        )
    )

    # -------------------------------------------------
    # Resume Understanding
    # -------------------------------------------------

    resume = (
        UnderstandingBuilder().build(
            document,
        )
    )

    # -------------------------------------------------
    # Job Understanding
    # -------------------------------------------------

    jd = (
        JobDescriptionParser().parse(
            JOB_DESCRIPTION,
        )
    )

    job = (
        JobUnderstandingBuilder().build(
            jd,
        )
    )

    # -------------------------------------------------
    # Gap Analysis
    # -------------------------------------------------

    gap = (
        GapAnalyzer().analyze(
            resume,
            job,
        )
    )

    # -------------------------------------------------
    # Planner
    # -------------------------------------------------

    blueprint = (
        Planner().build(
            document=document,
            resume=resume,
            job=job,
            gap=gap,
        )
    )

    # -------------------------------------------------
    # Optimizer
    # -------------------------------------------------

    result = (
        Optimizer().optimize(
            document,
            blueprint,
        )
    )

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    print("=" * 60)
    print("OPTIMIZATION RESULT")
    print("=" * 60)

    print()

    print(
        "Success:",
        result.success,
    )

    print(
        "Message:",
        result.message,
    )

    print()

    print(
        "Modified Sections:"
    )

    if result.modified_sections:

        for section in result.modified_sections:

            print(
                f"  • {section}"
            )

    else:

        print(
            "  None"
        )

    print()

    print(
        "Rewritten Sections:"
    )

    if result.rewritten_sections:

        for (
            section,
            content,
        ) in result.rewritten_sections.items():

            print()

            print(section)

            print("-" * 40)

            print(content)

    else:

        print(
            "  None"
        )


if __name__ == "__main__":
    main()