from __future__ import annotations

from docx.text.paragraph import Paragraph as DocxParagraph

from app.engine.models.document.numbering import Numbering


class NumberingReader:
    """
    Reads numbering and bullet information from a
    Word paragraph.

    Responsible ONLY for extracting numbering
    metadata from the underlying XML.
    """

    @staticmethod
    def read(
        paragraph: DocxParagraph,
    ) -> Numbering | None:

        p = paragraph._p
        pPr = p.pPr

        if pPr is None:
            return None

        numPr = pPr.numPr

        if numPr is None:
            return None

        num_id = None
        level = 0

        if numPr.numId is not None:
            num_id = int(numPr.numId.val)

        if numPr.ilvl is not None:
            level = int(numPr.ilvl.val)

        return Numbering(

            num_id=num_id,

            level=level,

            is_bulleted=False,

            is_numbered=True,

            format=None,

            text=None,

            restart=False,

        )




