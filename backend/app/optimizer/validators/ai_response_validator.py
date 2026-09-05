"""
app.optimizer.validators.ai_response_validator

Validates AI-generated paragraph updates.
"""

from __future__ import annotations

from app.optimizer.models.paragraph_update import (
    ParagraphUpdate,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)

class AIResponseValidator:
    """
    Validates AI response against the optimization contract.
    """
    def __init__(
        self,
        knowledge_manager: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge_manager

    def validate(
        self,
        updates: list[ParagraphUpdate],
        request,
    ) -> list[str]:
        """
        Validate AI paragraph updates against:

        - basic response structure
        - Planner-authorized paragraph IDs
        - exact original resume paragraph text
        - formatting safety
        - reasonable rewrite length
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

        # -----------------------------------------
        # Build authorized paragraph map
        # -----------------------------------------

        authorized_ids: set[str] = set()

        section_plan = (
            request.blueprint.section_plan
        )

        for paragraph_ids in (
            section_plan.paragraph_ids.values()
        ):
            authorized_ids.update(
                paragraph_ids
            )

        # -----------------------------------------
        # Original resume paragraphs
        # -----------------------------------------

        original_paragraphs = (
            request.document.paragraphs
        )

        seen_ids: set[str] = set()

        for update in updates:

            paragraph_id = (
                update.paragraph_id.strip()
            )

            # -------------------------------------
            # Paragraph ID
            # -------------------------------------

            if not paragraph_id:

                errors.append(
                    "Missing paragraph_id."
                )

            elif paragraph_id in seen_ids:

                errors.append(
                    f"Duplicate paragraph_id: "
                    f"{paragraph_id}"
                )

            else:

                seen_ids.add(
                    paragraph_id
                )

            # -------------------------------------
            # Authorization
            # -------------------------------------

            if paragraph_id and (
                paragraph_id
                not in authorized_ids
            ):

                errors.append(
                    f"{paragraph_id}: "
                    "paragraph is not authorized "
                    "by the Planner."
                )

            # -------------------------------------
            # Resolve paragraph index
            # -------------------------------------

            paragraph_index: int | None = None

            if paragraph_id.startswith("p"):

                try:

                    paragraph_index = int(
                        paragraph_id[1:]
                    )

                except ValueError:

                    paragraph_index = None

            if paragraph_index is not None:

                if not (
                    0
                    <= paragraph_index
                    < len(original_paragraphs)
                ):

                    errors.append(
                        f"{paragraph_id}: "
                        "paragraph does not exist "
                        "in the original document."
                    )

            # -------------------------------------
            # Section
            # -------------------------------------

            if not update.section.strip():

                errors.append(
                    f"{paragraph_id}: "
                    "section is empty."
                )

            # -------------------------------------
            # Original Text
            # -------------------------------------

            if not update.original_text.strip():

                errors.append(
                    f"{paragraph_id}: "
                    "original_text is empty."
                )

            # -------------------------------------
            # Exact Original Text Match
            # -------------------------------------

            if (
                paragraph_index is not None
                and 0
                <= paragraph_index
                < len(original_paragraphs)
            ):

                actual_original = (
                    original_paragraphs[
                        paragraph_index
                    ]
                )

                if (
                    update.original_text
                    != actual_original
                ):

                    errors.append(
                        f"{paragraph_id}: "
                        "original_text does not "
                        "exactly match the original "
                        "resume paragraph."
                    )

            # -------------------------------------
            # Optimized Text
            # -------------------------------------

            if not update.optimized_text.strip():

                errors.append(
                    f"{paragraph_id}: "
                    "optimized_text is empty."
                )

            # -------------------------------------
            # Confidence
            # -------------------------------------

            if not (
                0.0
                <= update.confidence
                <= 1.0
            ):

                errors.append(
                    f"{paragraph_id}: "
                    "confidence must be between "
                    "0 and 1."
                )

            # -------------------------------------
            # Formatting Safety
            # -------------------------------------

            if not update.formatting_safe:

                errors.append(
                    f"{paragraph_id}: "
                    "AI marked update as "
                    "formatting unsafe."
                )

            # -------------------------------------
            # Length Check
            # -------------------------------------

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
                        f"{paragraph_id}: "
                        "optimized text is "
                        "excessively longer "
                        "than the original."
                    )

            # -------------------------------------
            # Technology Authorization
            # -------------------------------------

            original_technologies = set(
                self._knowledge.extract(
                    update.original_text
                )
            )

            optimized_technologies = set(
                self._knowledge.extract(
                    update.optimized_text
                )
            )

            new_technologies = (
                optimized_technologies
                - original_technologies
            )

            knowledge = (
                request.blueprint.knowledge
            )

            authorized_technologies = {
                skill.canonical
                for skill in (
                    knowledge.optimization_skills
                )
            }

            unauthorized_technologies = (
                new_technologies
                - authorized_technologies
            )

            if unauthorized_technologies:

                errors.append(
                    f"{paragraph_id}: "
                    "optimized text introduces "
                    "unauthorized technologies: "
                    + ", ".join(
                        sorted(
                            unauthorized_technologies
                        )
                    )
                    + "."
                )

        return errors