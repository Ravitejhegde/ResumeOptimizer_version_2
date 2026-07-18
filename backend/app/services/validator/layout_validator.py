import re


class LayoutValidator:

    MAX_CHARACTER_CHANGE = 0.20
    MAX_WORD_CHANGE = 0.20

    @staticmethod
    def validate(
        original: str,
        optimized: str,
    ) -> tuple[bool, str]:

        original = original.strip()
        optimized = optimized.strip()

        if not original:
            return False, "Original paragraph is empty."

        if not optimized:
            return False, "Optimized paragraph is empty."

        original_characters = len(original)
        optimized_characters = len(optimized)

        character_change = abs(
            optimized_characters - original_characters
        ) / original_characters

        if character_change > LayoutValidator.MAX_CHARACTER_CHANGE:
            return (
                False,
                "Character count changed too much.",
            )

        original_words = len(
            re.findall(r"\S+", original)
        )

        optimized_words = len(
            re.findall(r"\S+", optimized)
        )

        word_change = abs(
            optimized_words - original_words
        ) / max(original_words, 1)

        if word_change > LayoutValidator.MAX_WORD_CHANGE:
            return (
                False,
                "Word count changed too much.",
            )

        return True, "Safe"