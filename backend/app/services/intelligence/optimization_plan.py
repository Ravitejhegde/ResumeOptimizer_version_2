@dataclass
class OptimizationPlan:

    target_role: str

    keep_sections: list[str]

    remove_sections: list[str]

    create_sections: list[str]

    keep_skills: list[str]

    remove_skills: list[str]

    add_skills: list[str]