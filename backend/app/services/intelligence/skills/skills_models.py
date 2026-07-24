from dataclasses import dataclass, field


@dataclass
class SkillCategoryGroup:

    name: str

    technologies: list[str] = field(
        default_factory=list
    )


@dataclass
class SkillsOptimizationInput:

    resume_categories: list[SkillCategoryGroup]

    jd_skills: list[str]

    selected_skills: list[str]

    max_lines: int

    target_role: str


@dataclass
class SkillsOptimizationResult:

    categories: list[SkillCategoryGroup]