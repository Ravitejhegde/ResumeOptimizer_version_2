from app.services.docx.document_block import DocumentBlock
from .character_budget import CharacterBudget


class CharacterBudgetAnalyzer:
    """
    Calculates how much text can safely remain inside
    a paragraph before it starts changing layout.
    """

    @staticmethod
    def analyze(
        block: DocumentBlock,
        optimized_text: str,
    ) -> CharacterBudget:

        return CharacterBudget.from_text(
            original_text=block.text,
            new_text=optimized_text,
        )