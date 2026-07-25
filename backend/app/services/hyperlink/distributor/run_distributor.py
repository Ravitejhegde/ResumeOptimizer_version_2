from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


class RunDistributor:
    """
    Distributes optimized text only into
    normal runs while preserving hyperlink runs.
    """

    @classmethod
    def distribute(
        cls,
        paragraph: Paragraph,
        new_text: str,
    ) -> None:

        normal_runs = []

        # -----------------------------------------
        # Collect only normal runs
        # -----------------------------------------

        for run in paragraph.runs:

            parent = run._element.getparent()

            if (
                parent is not None
                and parent.tag == qn("w:hyperlink")
            ):
                continue

            normal_runs.append(run)

        if not normal_runs:
            return

        # -----------------------------------------
        # Clear only normal runs
        # -----------------------------------------

        for run in normal_runs:
            run.text = ""

        # -----------------------------------------
        # Put optimized text into the first
        # normal run.
        #
        # Hyperlink runs remain untouched.
        # -----------------------------------------

        normal_runs[0].text = new_text