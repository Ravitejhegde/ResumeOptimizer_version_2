"""
app.writer.rewriters.run_distributor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replaces paragraph text while preserving the original
DOCX run structure and formatting.
"""

from __future__ import annotations

from docx.text.paragraph import Paragraph
from docx.text.run import Run


class RunDistributor:
    """
    Replaces paragraph content using the existing DOCX runs.

    The original DOCX is the formatting authority.

    Existing runs are reused so that their formatting,
    ordering, and special elements remain intact.
    """

    def distribute(
        self,
        paragraph: Paragraph,
        text: str,
    ) -> None:
        """
        Replace paragraph text while preserving the
        original run structure and formatting.
        """

        runs = list(paragraph.runs)

        if not runs:
            return

        if paragraph.text == text:
            return

        # -------------------------------------------------
        # Find existing tab runs.
        # -------------------------------------------------

        tab_indexes = [
            index
            for index, run in enumerate(runs)
            if self._contains_tab(run)
        ]

        # -------------------------------------------------
        # New text must contain the same tab structure.
        # -------------------------------------------------

        if text.count("\t") != len(tab_indexes):
            self._write_without_special_structure(
                runs,
                text,
            )
            return

        segments = text.split("\t")

        # -------------------------------------------------
        # Distribute each text segment into the existing
        # ordinary runs around the existing tab runs.
        # -------------------------------------------------

        segment_start = 0

        for segment_index, tab_index in enumerate(
            tab_indexes
        ):
            self._distribute_segment(
                runs=runs,
                start=segment_start,
                end=tab_index,
                text=segments[segment_index],
            )

            segment_start = tab_index + 1

        # -------------------------------------------------
        # Final segment after the last tab.
        # -------------------------------------------------

        self._distribute_segment(
            runs=runs,
            start=segment_start,
            end=len(runs),
            text=segments[-1],
        )

    # =====================================================
    # Segment distribution
    # =====================================================

    @classmethod
    def _distribute_segment(
        cls,
        runs: list[Run],
        start: int,
        end: int,
        text: str,
    ) -> None:
        """
        Distribute text across existing ordinary runs.

        The number of characters assigned to each run follows
        the original run text lengths as closely as possible.

        This preserves the original run formatting pattern.
        """

        ordinary_runs = [
            run
            for run in runs[start:end]
            if not cls._contains_tab(run)
        ]

        if not ordinary_runs:
            return

        # -------------------------------------------------
        # Original run lengths.
        #
        # We capture these BEFORE modifying anything.
        # -------------------------------------------------

        original_lengths = [
            len(run.text)
            for run in ordinary_runs
        ]

        # -------------------------------------------------
        # Remove text from existing runs while preserving
        # their XML text elements.
        # -------------------------------------------------

        for run in ordinary_runs:
            cls._clear_text_content(run)

        # -------------------------------------------------
        # If there is no new text, the runs remain empty.
        # -------------------------------------------------

        if not text:
            return

        # -------------------------------------------------
        # Calculate how much text each existing run receives.
        #
        # The original run boundaries are preserved as much
        # as possible.
        # -------------------------------------------------

        allocations = cls._calculate_allocations(
            original_lengths=original_lengths,
            text_length=len(text),
        )

        position = 0

        for run, length in zip(
            ordinary_runs,
            allocations,
        ):
            if length <= 0:
                continue

            chunk = text[
                position:position + length
            ]

            cls._set_existing_text(
                run,
                chunk,
            )

            position += length

        # -------------------------------------------------
        # If rounding left characters unassigned, append
        # them to the final ordinary run.
        # -------------------------------------------------

        if position < len(text):
            final_run = ordinary_runs[-1]

            remaining = text[position:]

            cls._set_existing_text(
                final_run,
                remaining,
                append=True,
            )

    # =====================================================
    # Allocation
    # =====================================================

    @staticmethod
    def _calculate_allocations(
        original_lengths: list[int],
        text_length: int,
    ) -> list[int]:
        """
        Calculate how many characters should be assigned
        to each existing run.

        The original run lengths act as the distribution
        pattern, while the total allocated characters equal
        the new text length.
        """

        if not original_lengths:
            return []

        total_original = sum(
            original_lengths
        )

        if total_original <= 0:
            allocations = [
                0
                for _ in original_lengths
            ]

            allocations[0] = text_length

            return allocations

        allocations: list[int] = []

        consumed = 0

        for index, original_length in enumerate(
            original_lengths
        ):
            if index == len(original_lengths) - 1:
                allocation = (
                    text_length - consumed
                )
            else:
                allocation = round(
                    text_length
                    * original_length
                    / total_original
                )

                allocation = max(
                    0,
                    allocation,
                )

            allocations.append(
                allocation
            )

            consumed += allocation

        return allocations

    # =====================================================
    # Tab detection
    # =====================================================

    @staticmethod
    def _contains_tab(
        run: Run,
    ) -> bool:
        """
        Return True when the run contains a native
        Word tab element.
        """

        for child in run._r:

            if child.tag.endswith("}tab"):
                return True

        return False

    # =====================================================
    # Text clearing
    # =====================================================

    @staticmethod
    def _clear_text_content(
        run: Run,
    ) -> None:
        """
        Clear textual content without removing the
        existing XML text elements.
        """

        text_elements = []

        for child in run._r:

            if child.tag.endswith("}t"):
                text_elements.append(child)

            elif child.tag.endswith("}delText"):
                text_elements.append(child)

            elif child.tag.endswith("}instrText"):
                text_elements.append(child)

        for element in text_elements:
            element.text = ""

    # =====================================================
    # Existing text setter
    # =====================================================

    @staticmethod
    def _set_existing_text(
        run: Run,
        text: str,
        append: bool = False,
    ) -> None:
        """
        Set text using an existing XML text element.

        This avoids reconstructing the run XML.
        """

        text_elements = [
            child
            for child in run._r
            if child.tag.endswith("}t")
        ]

        if not text_elements:
            run.text = text
            return

        target = text_elements[0]

        if append:
            current = target.text or ""
            target.text = current + text
        else:
            target.text = text

        for element in text_elements[1:]:
            element.text = ""

    # =====================================================
    # Fallback
    # =====================================================

    @classmethod
    def _write_without_special_structure(
        cls,
        runs: list[Run],
        text: str,
    ) -> None:
        """
        Fallback for incompatible special-character structure.

        Existing run XML is preserved as much as possible.
        """

        ordinary_runs = [
            run
            for run in runs
            if not cls._contains_tab(run)
        ]

        if not ordinary_runs:
            return

        for run in ordinary_runs:
            cls._clear_text_content(run)

        safe_text = text.replace(
            "\t",
            " ",
        )

        cls._distribute_segment(
            runs=ordinary_runs,
            start=0,
            end=len(ordinary_runs),
            text=safe_text,
        )