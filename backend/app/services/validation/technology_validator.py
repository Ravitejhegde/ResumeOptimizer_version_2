from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)

from app.services.validation.validation_result import (
    ValidationResult,
)


class TechnologyValidator:
    """
    Ensures the AI introduces only
    approved technologies.
    """

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
        allowed_additions: list[str],
    ) -> ValidationResult:

        result = ValidationResult()

        original = TechnologyDetector.detect(
            original_text
        )

        updated = TechnologyDetector.detect(
            updated_text
        )

        approved = [

            tech.lower()

            for tech in allowed_additions

        ]

        # -----------------------------------------
        # Detect new technologies
        # -----------------------------------------

        for technology in updated:

            if TechnologyMatcher.contains(
                original,
                technology,
            ):
                continue

            if technology.lower() in approved:
                continue

            result.add_error(

                f"Unauthorized technology added: {technology}"

            )

        result.details["original"] = original
        result.details["updated"] = updated
        result.details["approved"] = allowed_additions

        return result