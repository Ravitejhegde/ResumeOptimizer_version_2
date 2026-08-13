"""
Gap Analysis integration test.
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
from app.understanding.services.understanding_builder import (
    UnderstandingBuilder,
)

RESUME = r"tests\resources\sample_resume.docx"

JOB_DESCRIPTION = """
Backend Developer

Requirements

Python
FastAPI
Docker
Redis
JWT
Authentication
REST API
SQL
Microservices
"""


def main() -> None:

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

    jd = JobDescriptionParser().parse(
        JOB_DESCRIPTION,
    )

    job = JobUnderstandingBuilder().build(
        jd,
    )
    print("=" * 60)
    print("JOB UNDERSTANDING")
    print("=" * 60)

    print()

    print("Target Role:")
    print(job.target_role)

    print()

    print("Required Skills:")
    print(job.required_skills)

    print()

    print("Required Technologies:")
    print(job.required_technologies)

    print()
    
    gap = GapAnalyzer().analyze(
        resume,
        job,
    )

    print("=" * 60)
    print("GAP ANALYSIS")
    print("=" * 60)

    print()

    print("Overall Match:")
    print(gap.overall_match)

    print()

    print("Role Match:")
    print(gap.role_match)

    print()

    print("Matched Skills:")
    print(gap.matched_skills)

    print()

    print("Missing Skills:")
    print(gap.missing_skills)

    print()

    print("Matched Technologies:")
    print(gap.matched_technologies)

    print()

    print("Missing Technologies:")
    print(gap.missing_technologies)


if __name__ == "__main__":
    main()