from .run_formatter import (
    RunFormatter,
)


class RunTextDistributor:

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
        # ------------------------------------------

        editable = []

        for i, snapshot in enumerate(block.runs):

            if not snapshot.bold:
                editable.append(i)

        if not editable:
            editable = [len(runs) - 1]

        # ------------------------------------------
        # Original editable text lengths
        # ------------------------------------------

        original_lengths = []

        total_length = 0

        for i in editable:

            length = len(block.runs[i].text)

            if length <= 0:
                length = 1

            original_lengths.append(length)

            total_length += length

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

            share = original_lengths[position] / total_length

            characters = int(len(text) * share)

            end = start + characters

            # Avoid cutting a word in half
            while (
                end < len(text)
                and end > start
                and text[end] != " "
            ):
                end += 1

            runs[run_index].text = text[start:end].strip()

            start = end