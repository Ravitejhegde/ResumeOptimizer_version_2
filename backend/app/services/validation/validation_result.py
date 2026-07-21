from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """
    Result returned by every validator.
    """

    approved: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    details: dict = field(
        default_factory=dict
    )

    def add_error(
        self,
        message: str,
    ):

        self.approved = False

        self.errors.append(
            message
        )

    def add_warning(
        self,
        message: str,
    ):

        self.warnings.append(
            message
        )

    def merge(
        self,
        other: "ValidationResult",
    ):

        if not other.approved:
            self.approved = False

        self.errors.extend(
            other.errors
        )

        self.warnings.extend(
            other.warnings
        )

        self.details.update(
            other.details
        )

    @property
    def has_errors(
        self,
    ) -> bool:

        return len(self.errors) > 0

    @property
    def has_warnings(
        self,
    ) -> bool:

        return len(self.warnings) > 0