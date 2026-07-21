from docx.text.run import Run

from app.services.document.editor.run_mapper import (
    RunMapper,
)

from app.services.document.editor.text_replacer import (
    TextReplacer,
)


class RunEditor:
    """
    Edits existing runs without recreating them.

    Formatting stays untouched.
    """

    @classmethod
    def replace(
        cls,
        runs: list[Run],
        optimized_text: str,
    ) -> None:

        if not runs:
            return

        # -------------------------------------
        # Original text
        # -------------------------------------

        original = "".join(
            run.text
            for run in runs
        )

        new_text = TextReplacer.replace(
            original,
            optimized_text,
        )

        mapping = RunMapper.map(
            runs
        )

        # -------------------------------------
        # Rewrite runs
        # -------------------------------------

        for index, item in enumerate(mapping):

            run = runs[index]

            text = new_text[
                item.start:item.end
            ]

            run.text = text

        # -------------------------------------
        # Remaining text
        # -------------------------------------

        consumed = mapping[-1].end

        if len(new_text) > consumed:

            runs[-1].text += new_text[
                consumed:
            ]