from dataclasses import dataclass, field


@dataclass
class Experience:
    company: str = ""
    role: str = ""
    duration: str = ""


@dataclass
class Education:
    degree: str = ""
    institution: str = ""
    year: str = ""


@dataclass
class Project:
    name: str = ""
    description: str = ""


@dataclass
class ResumeProfile:
    name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""

    skills: list[str] = field(default_factory=list)

    experience: list[Experience] = field(default_factory=list)

    education: list[Education] = field(default_factory=list)

    projects: list[Project] = field(default_factory=list)




