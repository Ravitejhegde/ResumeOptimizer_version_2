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
        # Restore formatting FIRST
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
        # Find editable runs
        # ------------------------------------------

        editable = []

        for i, snapshot in enumerate(block.runs):

            if not snapshot.bold:

                editable.append(i)

        # ------------------------------------------
        # If every run is bold,
        # use the last run.
        # ------------------------------------------

        if not editable:

            editable = [len(runs) - 1]

        # ------------------------------------------
        # Clear editable runs
        # ------------------------------------------

        for i in editable:

            runs[i].text = ""

        # ------------------------------------------
        # Put ALL new text into first editable run
        # ------------------------------------------

        runs[editable[0]].text = block.text

        # ------------------------------------------
        # Keep locked runs untouched
        # ------------------------------------------