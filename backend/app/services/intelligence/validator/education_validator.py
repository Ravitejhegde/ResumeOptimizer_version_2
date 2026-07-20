from .validation_result import ValidationResult


class EducationValidator:

    @classmethod
    def validate(

        cls,

        original_blocks,

        updated_blocks,

    ) -> ValidationResult:

        result = ValidationResult()

        result.fixed_blocks = updated_blocks

        return result