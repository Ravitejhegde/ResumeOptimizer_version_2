"""
app.optimizer.validators.ai_response_validator

Validates AI-generated paragraph updates.
"""

from __future__ import annotations

from app.optimizer.models.paragraph_update import (
    ParagraphUpdate,
)


class AIResponseValidator:
    """
    Validates AI response before it is accepted
    by the Optimizer.
    """

    def validate(
        self,
        updates: list[ParagraphUpdate],
    ) -> list[str]:
        """
        Validate paragraph updates.

        Returns:
            List of validation errors.
        """

        errors: list[str] = []

        # -----------------------------------------
        # Empty Response
        # -----------------------------------------

        if not updates:

            errors.append(
                "AI returned no paragraph updates."
            )

            return errors

        seen_ids: set[str] = set()

        for update in updates:

            # -----------------------------------------
            # Paragraph ID
            # -----------------------------------------

            if not update.paragraph_id.strip():

                errors.append(
                    "Missing paragraph_id."
                )

            elif update.paragraph_id in seen_ids:

                errors.append(
                    f"Duplicate paragraph_id: "
                    f"{update.paragraph_id}"
                )

            else:

                seen_ids.add(
                    update.paragraph_id
                )

            # -----------------------------------------
            # Section
            # -----------------------------------------

            if not update.section.strip():

                errors.append(
                    f"{update.paragraph_id}: "
                    "section is empty."
                )

            # -----------------------------------------
            # Original Text
            # -----------------------------------------

            if not update.original_text.strip():

                errors.append(
                    f"{update.paragraph_id}: "
                    "original_text is empty."
                )

            # -----------------------------------------
            # Optimized Text
            # -----------------------------------------

            if not update.optimized_text.strip():

                errors.append(
                    f"{update.paragraph_id}: "
                    "optimized_text is empty."
                )

            # -----------------------------------------
            # Confidence
            # -----------------------------------------

            if not (
                0.0
                <= update.confidence
                <= 1.0
            ):

                errors.append(
                    f"{update.paragraph_id}: "
                    "confidence must be between 0 and 1."
                )

            # -----------------------------------------
            # Formatting Safety
            # -----------------------------------------

            if not update.formatting_safe:

                errors.append(
                    f"{update.paragraph_id}: "
                    "AI marked update as formatting unsafe."
                )

            # -----------------------------------------
            # Length Check
            # -----------------------------------------

            if (
                update.original_text.strip()
                and update.optimized_text.strip()
            ):

                ratio = (
                    len(update.optimized_text)
                    / max(
                        len(update.original_text),
                        1,
                    )
                )

                if ratio > 3.0:

                    errors.append(
                        f"{update.paragraph_id}: "
                        "optimized text is excessively longer than the original."
                    )

        return errors