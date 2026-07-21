import re

from app.services.validation.validation_result import (
    ValidationResult,
)


class EducationValidator:
    """
    Prevents the AI from changing
    education qualifications.
    """

    DEGREE_PATTERN = re.compile(

        r"\b("
        r"B\.?E|B\.?Tech|B\.?Sc|BCA|BBA|BA|BCom|"
        r"M\.?E|M\.?Tech|MCA|MBA|MSc|MA|PhD|Diploma"
        r")\b",

        flags=re.IGNORECASE,

    )

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
    ) -> ValidationResult:

        result = ValidationResult()

        original = {

            degree.upper()

            for degree in cls.DEGREE_PATTERN.findall(
                original_text
            )

        }

        updated = {

            degree.upper()

            for degree in cls.DEGREE_PATTERN.findall(
                updated_text
            )

        }

        added = updated - original

        removed = original - updated

        if added:

            result.add_error(

                "AI introduced education qualification(s): "
                + ", ".join(sorted(added))

            )

        if removed:

            result.add_error(

                "Education qualification removed: "
                + ", ".join(sorted(removed))

            )

        result.details["original_degrees"] = sorted(original)
        result.details["updated_degrees"] = sorted(updated)

        return result