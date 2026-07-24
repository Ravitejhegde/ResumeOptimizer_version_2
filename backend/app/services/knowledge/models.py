from dataclasses import dataclass, field


@dataclass
class ResumeSection:
    title: str
    paragraphs: list[str] = field(default_factory=list)


@dataclass
class ResumeKnowledge:
    summary: str = ""

    skills: list[str] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)

    sections: list[ResumeSection] = field(default_factory=list)

    total_sections: int = 0
    total_skills: int = 0
    total_projects: int = 0
    total_experience: int = 0
    total_education: int = 0

    detected_email: str = ""
    detected_phone: str = ""
    detected_name: str = ""

    has_summary: bool = False
    has_projects: bool = False
    has_certifications: bool = False