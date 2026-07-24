from dataclasses import dataclass


@dataclass(slots=True)
class CharacterBudget:
    """
    Represents the character capacity of a paragraph.
    """

    original_length: int
    current_length: int
    remaining: int
    can_expand: bool

    @classmethod
    def from_text(
        cls,
        original_text: str,
        new_text: str,
    ) -> "CharacterBudget":

        original_length = len(original_text)
        current_length = len(new_text)

        remaining = original_length - current_length

        return cls(
            original_length=original_length,
            current_length=current_length,
            remaining=remaining,
            can_expand=remaining > 0,
        )