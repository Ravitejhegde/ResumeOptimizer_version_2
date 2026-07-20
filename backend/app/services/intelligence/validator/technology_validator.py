from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
)

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)

from app.services.intelligence.validator.validation_result import (
    ValidationResult,
)


class TechnologyValidator:
    """
    Validates all technologies produced by the AI.

    Responsibilities
    ----------------
    ✓ Unknown technology detection
    ✓ Alias normalization
    ✓ Duplicate removal
    ✓ Canonical naming
    """

    @classmethod
    def validate(
        cls,
        blocks,
    ) -> ValidationResult:

        result = ValidationResult()

        result.fixed_blocks = []

        known = {

            tech["name"].lower()

            for tech in KnowledgeEngine.technologies()

        }

        for block in blocks:

            technologies = []

            words = block.text.replace(
                "\n",
                " ",
            ).split(",")

            for word in words:

                value = word.strip()

                if not value:
                    continue

                canonical = TechnologyMatcher.normalize_list(
                    [value]
                )[0]

                if canonical.lower() in known:

                    technologies.append(
                        canonical
                    )

            technologies = TechnologyMatcher.normalize_list(
                technologies
            )

            block.detected_technologies = technologies

            result.fixed_blocks.append(
                block
            )

        return result