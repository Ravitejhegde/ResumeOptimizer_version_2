import re

from app.services.intelligence.validator.validation_result import (
    ValidationResult,
)


class FactValidator:
    """
    Prevents the AI from changing factual information.
    """

    LOCKED_PATTERNS = [

        # CGPA
        r"\bCGPA\b.*",

        # Percentage
        r"\b\d+(\.\d+)?%\b",

        # Years
        r"\b(19|20)\d{2}\b",

        # Month Year
        r"(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)\s+\d{4}",

    ]

    @classmethod
    def validate(

        cls,

        original_blocks,

        optimized_blocks,

    ) -> ValidationResult:

        result = ValidationResult()

        result.fixed_blocks = []

        original_map = {

            block.id: block

            for block in original_blocks

        }

        for block in optimized_blocks:

            original = original_map.get(
                block.id
            )

            if original is None:

                result.errors.append(

                    f"Unknown block id {block.id}"

                )

                result.passed = False

                continue

            if cls._contains_locked_change(

                original.text,

                block.text,

            ):

                result.errors.append(

                    f"Locked facts changed in block {block.id}"

                )

                result.passed = False

                result.fixed_blocks.append(
                    original
                )

            else:

                result.fixed_blocks.append(
                    block
                )

        return result

    @classmethod
    def _contains_locked_change(

        cls,

        original,

        updated,

    ) -> bool:

        for pattern in cls.LOCKED_PATTERNS:

            original_match = re.findall(

                pattern,

                original,

                flags=re.IGNORECASE,

            )

            updated_match = re.findall(

                pattern,

                updated,

                flags=re.IGNORECASE,

            )

            if original_match != updated_match:

                return True

        return False