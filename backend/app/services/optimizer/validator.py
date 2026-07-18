from app.services.optimizer.optimization_map import (
    OptimizationMap,
)


class OptimizationValidator:

    MAX_LENGTH_CHANGE = 0.30

    @staticmethod
    def validate(
        item: OptimizationMap,
    ) -> tuple[bool, str]:

        original = item.original_text.strip()

        optimized = item.optimized_text.strip()

        if not optimized:

            return False, "Optimized text is empty."

        if not original:

            return False, "Original text is empty."

        original_length = len(original)

        optimized_length = len(optimized)

        difference = abs(

            optimized_length - original_length

        ) / original_length

        if difference > OptimizationValidator.MAX_LENGTH_CHANGE:

            return (

                False,

                "Paragraph length changed too much.",

            )

        return True, "Safe"