from app.services.intelligence.validator.approval import (
    Approval,
)

from app.services.intelligence.validator.fact_validator import (
    FactValidator,
)

from app.services.intelligence.validator.technology_validator import (
    TechnologyValidator,
)

from app.services.intelligence.validator.duplicate_cleaner import (
    DuplicateCleaner,
)

from app.services.intelligence.validator.grammar_validator import (
    GrammarValidator,
)


class QualityGate:
    """
    Final Brain v3 Quality Gate.

    Pipeline

        AI Response
              │
              ▼
        Fact Validation
              ▼
        Technology Validation
              ▼
        Duplicate Cleaner
              ▼
        Grammar Validator
              ▼
        Approval
    """

    @classmethod
    def approve(
        cls,
        original_blocks,
        optimized_blocks,
    ):

        approval = Approval()

        # ------------------------------------
        # Fact Validation
        # ------------------------------------

        fact = FactValidator.validate(
            original_blocks,
            optimized_blocks,
        )

        approval.errors.extend(
            fact.errors
        )

        approval.warnings.extend(
            fact.warnings
        )

        blocks = fact.fixed_blocks

        if not fact.passed:

            approval.approved = False
            approval.retry = True

            return approval, blocks

        # ------------------------------------
        # Technology Validation
        # ------------------------------------

        tech = TechnologyValidator.validate(
            blocks,
        )

        approval.errors.extend(
            tech.errors
        )

        approval.warnings.extend(
            tech.warnings
        )

        blocks = tech.fixed_blocks

        # ------------------------------------
        # Duplicate Cleaning
        # ------------------------------------

        blocks = DuplicateCleaner.clean(
            blocks
        )

        approval.auto_fixed = True

        # ------------------------------------
        # Grammar Validation
        # ------------------------------------

        grammar = GrammarValidator.validate(
            blocks
        )

        approval.errors.extend(
            grammar.errors
        )

        approval.warnings.extend(
            grammar.warnings
        )

        blocks = grammar.fixed_blocks

        # ------------------------------------
        # Final Decision
        # ------------------------------------

        if approval.errors:

            approval.approved = False
            approval.retry = True

        return approval, blocks