"""
Analyzer integration test.
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

RESUME = r"tests\resources\sample_resume.docx"


def main() -> None:

    document = DocumentAnalyzer().analyze(
        RESUME
    )

    document = SectionAnalyzer().analyze(
        document
    )

    document = TechnologyAnalyzer().analyze(
        document
    )

    document = SkillAnalyzer().analyze(
        document
    )

    document = RoleAnalyzer().analyze(
        document
    )

    document = ExperienceAnalyzer().analyze(
        document
    )

    document = ProjectAnalyzer().analyze(
        document
    )

    print("=" * 60)
    print("ANALYZER SUMMARY")
    print("=" * 60)

    print()

    print("Technologies:")
    print(sorted(document.technologies.keys()))

    print()

    print("Skills:")
    print(sorted(document.skills.keys()))

    print()

    print("Roles:")
    print(sorted(document.roles.keys()))

    print()

    print("Experiences:")
    print(len(document.experiences))

    print()

    print("Projects:")
    print(len(document.projects))


if __name__ == "__main__":
    main()