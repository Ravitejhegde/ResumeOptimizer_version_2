import re

from app.services.validation.validation_result import (
    ValidationResult,
)


class DateValidator:
    """
    Prevents the AI from changing
    employment and education dates.
    """

    YEAR_PATTERN = re.compile(
        r"\b(19|20)\d{2}\b"
    )

    RANGE_PATTERN = re.compile(
        r"\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b"
    )

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
    ) -> ValidationResult:

        result = ValidationResult()

        original_years = sorted(
            cls.YEAR_PATTERN.findall(
                original_text
            )
        )

        updated_years = sorted(
            cls.YEAR_PATTERN.findall(
                updated_text
            )
        )

        if original_years != updated_years:

            result.add_error(
                "Employment or education years were modified."
            )

        original_ranges = sorted(
            cls.RANGE_PATTERN.findall(
                original_text
            )
        )

        updated_ranges = sorted(
            cls.RANGE_PATTERN.findall(
                updated_text
            )
        )

        if original_ranges != updated_ranges:

            result.add_error(
                "Date ranges were modified."
            )

        result.details["original_years"] = original_years
        result.details["updated_years"] = updated_years

        return result