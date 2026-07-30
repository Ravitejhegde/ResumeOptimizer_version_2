from __future__ import annotations

from dataclasses import dataclass



@dataclass(slots=True)
class LengthBudget:
    """
    Represents allowed content growth.

    Used by AI prompt generation and
    later response validation.

    Example:

        Original:
            20 words

        Allowed:
            27 words

        Growth ratio:
            1.35
    """

    original_words: int

    max_words: int

    growth_ratio: float



class LengthController:
    """
    Controls AI output size.

    Responsibilities:

        - Calculate safe expansion limits.
        - Prevent unnecessarily long AI responses.
        - Create length instructions.


    Does NOT:

        - Validate final AI response.
        - Modify content.
        - Call AI.


    Note:

        Final AI response length validation
        will be implemented later as a
        separate validator.
    """



    DEFAULT_GROWTH_RATIO = 1.35



    def calculate_budget(
        self,
        text: str,
        growth_ratio: float | None = None,
    ) -> LengthBudget:
        """
        Calculate allowed output size.

        Formula:

            maximum_words =
            original_words * growth_ratio


        Default:

            35% expansion allowed.
        """


        ratio = (
            growth_ratio
            if growth_ratio is not None
            else self.DEFAULT_GROWTH_RATIO
        )


        original_words = (
            self._word_count(
                text
            )
        )


        max_words = max(
            original_words,
            int(
                original_words * ratio
            ),
        )


        return LengthBudget(

            original_words=original_words,

            max_words=max_words,

            growth_ratio=ratio,

        )



    def create_instruction(
        self,
        budget: LengthBudget,
    ) -> str:
        """
        Convert budget into AI instruction.
        """


        return (
            "Keep rewritten content concise. "
            f"Original length: "
            f"{budget.original_words} words. "
            f"Maximum allowed length: "
            f"{budget.max_words} words. "
            "Do not add unnecessary details."
        )



    def calculate_multiple(
        self,
        sections: dict[str, str],
        growth_ratio: float | None = None,
    ) -> dict[str, LengthBudget]:
        """
        Calculate budgets for multiple sections.

        Example:

            summary
            experience
            projects
        """


        return {

            name: self.calculate_budget(
                text,
                growth_ratio,
            )

            for name, text in sections.items()

        }



    @staticmethod
    def _word_count(
        text: str,
    ) -> int:
        """
        Count words safely.
        """

        if not text:

            return 0


        return len(
            text.split()
        )