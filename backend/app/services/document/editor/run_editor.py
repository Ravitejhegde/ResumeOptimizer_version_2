from docx.oxml.ns import qn
from docx.text.run import Run


class RunEditor:
    """
    Replaces paragraph text while preserving formatting
    and leaving hyperlink runs untouched.
    """

    @staticmethod
    def _is_hyperlink_run(run: Run) -> bool:

        parent = run._element.getparent()

        return (
            parent is not None
            and parent.tag == qn("w:hyperlink")
        )

    @classmethod
    def replace(
        cls,
        runs: list[Run],
        optimized_text: str,
    ) -> None:

        if not runs:
            return

        # -----------------------------------------
        # Editable runs (ignore hyperlink runs)
        # -----------------------------------------

        editable_runs = [

            run

            for run in runs

            if not cls._is_hyperlink_run(run)

        ]

        if not editable_runs:
            return

        # -----------------------------------------
        # Put new text into first editable run
        # -----------------------------------------

        editable_runs[0].text = optimized_text.strip()

        # -----------------------------------------
        # Clear remaining editable runs
        # -----------------------------------------

        for run in editable_runs[1:]:

            run.text = ""