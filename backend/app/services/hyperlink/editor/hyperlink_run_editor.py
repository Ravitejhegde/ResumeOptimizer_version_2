from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkRunEditor:
    """
    Restores formatting for every run
    inside a hyperlink.

    This class never changes:
    - URL
    - Relationship ID
    - Hyperlink XML

    It only restores character formatting.
    """

    @classmethod
    def restore(
        cls,
        paragraph: Paragraph,
        hyperlink: Hyperlink,
    ) -> None:

        paragraph_xml = paragraph._p

        for node in paragraph_xml:

            if node.tag != qn("w:hyperlink"):
                continue

            if (
                node.get(qn("r:id"), "")
                != hyperlink.relationship_id
            ):
                continue

            run_index = 0

            for run_xml in node.findall(qn("w:r")):

                if run_index >= len(hyperlink.runs):
                    break

                run = paragraph.runs[
                    hyperlink.runs[run_index].run_index
                ]

                model = hyperlink.runs[run_index]

                font = run.font

                font.bold = model.bold

                font.italic = model.italic

                font.underline = model.underline

                font.name = model.font_name

                if model.font_size:

                    font.size = Pt(
                        model.font_size
                    )

                if model.color:

                    try:

                        font.color.rgb = (
                            RGBColor.from_string(
                                model.color.replace(
                                    "#",
                                    "",
                                )
                            )
                        )

                    except Exception:

                        pass

                try:

                    if model.style:

                        run.style = model.style

                except Exception:

                    pass

                run_index += 1

            break