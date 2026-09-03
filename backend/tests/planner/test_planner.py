"""
Planner integration test.
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

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)
from app.knowledge.builder.knowledge_builder import (
    KnowledgeBuilder,
)

from app.planner.services.planner import (
    Planner,
)

from app.understanding.services.understanding_builder import (
    UnderstandingBuilder,
)


RESUME = r"tests\resources\sample_resume.docx"


JOB_DESCRIPTION = """
Backend Developer

Requirements

Python
FastAPI
REST API
Docker
JWT
Authentication
Redis
SQL
"""


def test_planner_integration() -> None:

    # -------------------------------------------------
    # Resume Pipeline
    # -------------------------------------------------

    document = DocumentAnalyzer().analyze(
        RESUME,
    )

    document = SectionAnalyzer().analyze(
        document,
    )

    document = TechnologyAnalyzer().analyze(
        document,
    )

    document = SkillAnalyzer().analyze(
        document,
    )

    document = RoleAnalyzer().analyze(
        document,
    )

    document = ExperienceAnalyzer().analyze(
        document,
    )

    document = ProjectAnalyzer().analyze(
        document,
    )

    resume = UnderstandingBuilder().build(
        document,
    )

    # -------------------------------------------------
    # Job Pipeline
    # -------------------------------------------------

    jd = JobDescriptionParser().parse(
        JOB_DESCRIPTION,
    )

    job = JobUnderstandingBuilder().build(
        jd,
    )

    # -------------------------------------------------
    # Gap Analysis
    # -------------------------------------------------

    gap = GapAnalyzer().analyze(
        resume,
        job,
    )

    # -------------------------------------------------
    # Knowledge Builder
    # -------------------------------------------------

    knowledge_manager = KnowledgeManager()

    knowledge = KnowledgeBuilder(
        knowledge_manager,
    ).build(
        role_id="backend_developer",
        matched_skills=gap.matched_skills,
        selected_missing_skills=[
            "Docker",
        ],
    )

    # -------------------------------------------------
    # Planner
    # -------------------------------------------------

    blueprint = Planner().build(
        document=document,
        resume=resume,
        job=job,
        gap=gap,
        knowledge=knowledge,
    )

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    print("=" * 60)
    print("PLANNER BLUEPRINT")
    print("=" * 60)
    print()

    print("Goal")
    print("-" * 60)
    print(blueprint.goal)
    print()

    print("Decision")
    print("-" * 60)
    print(blueprint.decision)
    print()

    print("Priorities")
    print("-" * 60)
    print(blueprint.priorities)
    print()

    print("Evidence")
    print("-" * 60)
    print(blueprint.evidence)
    print()

    print("Section Plan")
    print("-" * 60)
    print(blueprint.section_plan)
    print()

    print("Rewrite Plan")
    print("-" * 60)
    print(blueprint.rewrite_plan)
    print()

    print("Prompt Plan")
    print("-" * 60)
    print(blueprint.prompt_plan)


