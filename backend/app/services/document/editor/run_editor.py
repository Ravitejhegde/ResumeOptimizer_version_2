from docx.text.run import Run


class RunEditor:
    """
    Replaces paragraph text while preserving
    paragraph formatting.

    The first run keeps its original formatting.
    Remaining runs are cleared.
    """

    @classmethod
    def replace(
        cls,
        runs: list[Run],
        optimized_text: str,
    ):

        if not runs:
            return

        runs[0].text = optimized_text.strip()

        for run in runs[1:]:
            run.text = ""