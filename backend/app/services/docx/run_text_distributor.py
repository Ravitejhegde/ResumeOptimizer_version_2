from docx.oxml.ns import qn

from .run_formatter import (
    RunFormatter,
)


class RunTextDistributor:

    @staticmethod
    def _is_hyperlink_run(run) -> bool:
        """
        Returns True if this run belongs to a hyperlink.
        """

        parent = run._element.getparent()

        return (
            parent is not None
            and parent.tag == qn("w:hyperlink")
        )

    @staticmethod
    def _editable_runs(paragraph):

        editable = []

        for index, run in enumerate(paragraph.runs):

            if RunTextDistributor._is_hyperlink_run(run):
                continue

            editable.append(index)

        return editable

    @staticmethod
    def distribute(
        paragraph,
        block,
    ):

        runs = paragraph.runs

        if not runs:
            paragraph.add_run(block.text)
            return

        # ------------------------------------------
        # Restore original formatting
        # ------------------------------------------

        for i, run in enumerate(runs):

            if i < len(block.runs):

                RunFormatter.restore(
                    run,
                    block.runs[i],
                )

        # ------------------------------------------
        # Locked paragraph
        # ------------------------------------------

        if not block.can_optimize:
            return

        # ------------------------------------------
        # Editable runs
        # (Hyperlink runs are skipped)
        # ------------------------------------------

        editable = RunTextDistributor._editable_runs(
            paragraph
        )

        if not editable:
            return

        # ------------------------------------------
        # Original editable text lengths
        # ------------------------------------------

        original_lengths = []

        total_length = 0

        for i in editable:

            if i >= len(block.runs):
                continue

            length = len(block.runs[i].text)

            if length <= 0:
                length = 1

            original_lengths.append(length)

            total_length += length

        if total_length == 0:
            total_length = 1

        # ------------------------------------------
        # Clear editable runs
        # ------------------------------------------

        for i in editable:

            runs[i].text = ""

        text = block.text

        start = 0

        # ------------------------------------------
        # Distribute proportionally
        # ------------------------------------------

        for position, run_index in enumerate(editable):

            if position == len(editable) - 1:

                runs[run_index].text = text[start:]

                break

            share = (
                original_lengths[position]
                / total_length
            )

            characters = int(
                len(text) * share
            )

            end = start + characters

            while (
                end < len(text)
                and end > start
                and text[end] != " "
            ):
                end += 1

            runs[run_index].text = (
                text[start:end].strip()
            )

            start = end