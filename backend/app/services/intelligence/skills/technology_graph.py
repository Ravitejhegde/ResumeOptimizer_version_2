from dataclasses import dataclass, field


@dataclass(frozen=True)
class Technology:

    name: str

    category: str

    roles: list[str] = field(
        default_factory=list
    )

    related: list[str] = field(
        default_factory=list
    )

    priority: int = 50


TECHNOLOGY_GRAPH = {

    "Python": Technology(

        name="Python",

        category="Programming Languages",

        roles=[
            "Backend Developer",
            "Full Stack Developer",
            "AI Engineer",
            "Data Engineer",
        ],

        related=[
            "FastAPI",
            "Django",
            "Flask",
            "REST API",
            "PostgreSQL",
        ],

        priority=100,

    ),

    "FastAPI": Technology(

        name="FastAPI",

        category="Backend Technologies",

        roles=[
            "Backend Developer",
            "Full Stack Developer",
        ],

        related=[
            "Python",
            "REST API",
            "JWT",
            "Swagger",
            "Docker",
        ],

        priority=98,

    ),

    "REST API": Technology(

        name="REST API",

        category="Backend Technologies",

        roles=[
            "Backend Developer",
            "Full Stack Developer",
        ],

        related=[
            "FastAPI",
            "JWT",
            "Swagger",
        ],

        priority=96,

    ),

    "PostgreSQL": Technology(

        name="PostgreSQL",

        category="Database",

        roles=[
            "Backend Developer",
            "Full Stack Developer",
        ],

        related=[
            "SQL",
            "Docker",
        ],

        priority=92,

    ),

    "Docker": Technology(

        name="Docker",

        category="Cloud & DevOps",

        roles=[
            "Backend Developer",
            "DevOps Engineer",
            "Full Stack Developer",
        ],

        related=[
            "AWS",
            "CI/CD",
            "Kubernetes",
        ],

        priority=90,

    ),

    "AWS": Technology(

        name="AWS",

        category="Cloud & DevOps",

        roles=[
            "Backend Developer",
            "Cloud Engineer",
        ],

        related=[
            "Docker",
            "CI/CD",
        ],

        priority=88,

    ),

    "Git": Technology(

        name="Git",

        category="Tools & Platforms",

        roles=[
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
        ],

        related=[
            "GitHub",
        ],

        priority=70,

    ),

    "GitHub": Technology(

        name="GitHub",

        category="Tools & Platforms",

        roles=[
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
        ],

        related=[
            "Git",
        ],

        priority=68,

    ),

}