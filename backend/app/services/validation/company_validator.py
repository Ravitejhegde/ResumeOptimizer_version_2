import re

from app.services.validation.validation_result import (
    ValidationResult,
)


class CompanyValidator:
    """
    Prevents the AI from inventing or replacing
    company names.
    """

    COMPANY_PATTERN = re.compile(
        r"\b(?:at|@)\s+([A-Z][A-Za-z0-9&.,\-\s]+)",
        flags=re.IGNORECASE,
    )

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
    ) -> ValidationResult:

        result = ValidationResult()

        original = set(
            match.strip()
            for match in cls.COMPANY_PATTERN.findall(
                original_text
            )
        )

        updated = set(
            match.strip()
            for match in cls.COMPANY_PATTERN.findall(
                updated_text
            )
        )

        # -----------------------------------------
        # New company invented
        # -----------------------------------------

        added = updated - original

        if added:

            result.add_error(

                "AI introduced new company name(s): "
                + ", ".join(sorted(added))

            )

        # -----------------------------------------
        # Existing company removed
        # -----------------------------------------

        removed = original - updated

        if removed:

            result.add_warning(

                "Existing company name removed: "
                + ", ".join(sorted(removed))

            )

        result.details["original_companies"] = sorted(original)
        result.details["updated_companies"] = sorted(updated)

        return result