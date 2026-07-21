from dataclasses import dataclass, field


@dataclass
class ResumeKnowledge:
    """
    Central knowledge extracted from a resume.

    This is the object consumed by the
    Intelligence Engine.
    """

    # Candidate

    name: str = ""

    email: str = ""

    phone: str = ""

    location: str = ""

    linkedin: str = ""

    github: str = ""

    portfolio: str = ""

    # Resume

    title: str = ""

    summary: str = ""

    detected_role: str = ""

    # Skills

    technologies: list[str] = field(
        default_factory=list
    )

    frameworks: list[str] = field(
        default_factory=list
    )

    programming_languages: list[str] = field(
        default_factory=list
    )

    databases: list[str] = field(
        default_factory=list
    )

    cloud: list[str] = field(
        default_factory=list
    )

    devops: list[str] = field(
        default_factory=list
    )

    tools: list[str] = field(
        default_factory=list
    )

    soft_skills: list[str] = field(
        default_factory=list
    )

    # Sections

    experience: list[str] = field(
        default_factory=list
    )

    projects: list[str] = field(
        default_factory=list
    )

    education: list[str] = field(
        default_factory=list
    )

    certifications: list[str] = field(
        default_factory=list
    )

    achievements: list[str] = field(
        default_factory=list
    )

    keywords: list[str] = field(
        default_factory=list
    )