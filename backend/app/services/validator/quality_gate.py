from app.services.validator.layout_validator import (
    LayoutValidator,
)

from app.services.validator.fact_validator import (
    FactValidator,
)


class ValidationEngine:

    @staticmethod
    def validate(
        original: str,
        optimized: str,
    ) -> tuple[bool, str]:

        # --------------------------
        # Layout Validation
        # --------------------------

        valid, reason = LayoutValidator.validate(
            original,
            optimized,
        )

        if not valid:

            return False, reason

        # --------------------------
        # Fact Validation
        # --------------------------

        valid, reason = FactValidator.validate(
            original,
            optimized,
        )

        if not valid:

            return False, reason

        return True, "Safe"