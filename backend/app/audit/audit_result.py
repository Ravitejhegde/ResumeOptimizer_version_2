from dataclasses import dataclass, field


@dataclass
class AuditResult:
    """
    Stores the complete Brain audit report.
    """

    resume_role: str = ""

    jd_role: str = ""

    matched_skills: list[str] = field(
        default_factory=list
    )

    missing_skills: list[str] = field(
        default_factory=list
    )

    extra_skills: list[str] = field(
        default_factory=list
    )

    recommendations: list[str] = field(
        default_factory=list
    )

    risks: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    validation_errors: list[str] = field(
        default_factory=list
    )

    score: int = 100

    def add_warning(
        self,
        message: str,
    ):

        self.warnings.append(
            message
        )

    def add_error(
        self,
        message: str,
    ):

        self.validation_errors.append(
            message
        )

    @property
    def passed(
        self,
    ) -> bool:

        return len(
            self.validation_errors
        ) == 0




