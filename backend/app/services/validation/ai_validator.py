from app.services.validation.validation_result import (
    ValidationResult,
)

from app.services.validation.company_validator import (
    CompanyValidator,
)

from app.services.validation.date_validator import (
    DateValidator,
)

from app.services.validation.education_validator import (
    EducationValidator,
)

from app.services.validation.technology_validator import (
    TechnologyValidator,
)

from app.services.validation.project_validator import (
    ProjectValidator,
)


class AIValidator:
    """
    Master validator that executes all
    AI safety checks before merging.
    """

    @classmethod
    def validate(
        cls,
        original_text: str,
        updated_text: str,
        allowed_additions: list[str],
    ) -> ValidationResult:

        result = ValidationResult()

        result.merge(

            CompanyValidator.validate(

                original_text,

                updated_text,

            )

        )

        result.merge(

            DateValidator.validate(

                original_text,

                updated_text,

            )

        )

        result.merge(

            EducationValidator.validate(

                original_text,

                updated_text,

            )

        )

        result.merge(

            TechnologyValidator.validate(

                original_text,

                updated_text,

                allowed_additions,

            )

        )

        result.merge(

            ProjectValidator.validate(

                original_text,

                updated_text,

            )

        )

        return result