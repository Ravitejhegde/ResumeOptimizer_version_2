"""
Understanding integration test.
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
from app.understanding.services.understanding_builder import (
    UnderstandingBuilder,
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

    understanding = (
        UnderstandingBuilder().build(
            document
        )
    )

    print("=" * 60)
    print("RESUME UNDERSTANDING")
    print("=" * 60)

    print()

    print("Primary Role:")
    print(understanding.primary_role)

    print()

    print("Secondary Roles:")
    print(understanding.secondary_roles)

    print()

    print("Primary Skills:")
    print(understanding.primary_skills)

    print()

    print("Primary Technologies:")
    print(understanding.primary_technologies)

    print()

    print("Strongest Experience:")
    print(understanding.strongest_experience)

    print()

    print("Strongest Project:")
    print(understanding.strongest_project)

    print()

    print("Summary:")
    print(repr(understanding.summary))

    print()

    print("Characters around '5':")
    index = understanding.summary.index("5")
    for i, c in enumerate(understanding.summary[max(0, index - 5):index + 15]):
        print(i, repr(c), ord(c))


if __name__ == "__main__":
    main()