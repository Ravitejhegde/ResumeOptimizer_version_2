from dataclasses import dataclass, field


@dataclass
class ValidationResult:

    passed: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    fixed_blocks: list[dict] = field(
        default_factory=list
    )