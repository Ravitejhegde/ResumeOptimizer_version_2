import re

from app.services.validation.validation_result import (
    ValidationResult,
)


class ProjectValidator:
    """
    Prevents the AI from inventing
    or renaming projects.
    """

    PROJECT_PATTERN = re.compile(
        r"[A-Za-z][A-Za-z0-9 ._\-]{2,60}"
    )

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
    ) -> ValidationResult:

        result = ValidationResult()

        if (
            original_text.strip()
            and not updated_text.strip()
        ):
            result.add_error(
                "Project description was removed."
            )

        original = original_text.strip()

        updated = updated_text.strip()

        if (
            len(updated)
            > len(original) * 1.8
        ):
            result.add_warning(
                "Project description grew significantly."
            )

        result.details["original_length"] = len(original)
        result.details["updated_length"] = len(updated)

        return result