from __future__ import annotations

from docx.text.paragraph import (
    Paragraph as DocxParagraph,
)

from app.engine.models.document.numbering import (
    Numbering,
)


class NumberingReader:
    """
    Reads Word numbering and bullet metadata.

    Responsibilities:
        - Detect list information.
        - Extract numbering id.
        - Extract nesting level.

    This reader:
        - Does not modify the document.
        - Does not generate visible numbering text.
    """

    @staticmethod
    def read(
        paragraph: DocxParagraph,
    ) -> Numbering | None:
        """
        Extract numbering information from paragraph.

        Returns:
            Numbering model or None.
        """

        p_properties = paragraph._p.pPr

        if p_properties is None:
            return None


        numbering_properties = (
            p_properties.numPr
        )

        if numbering_properties is None:
            return None


        num_id = None

        level = 0


        if numbering_properties.numId is not None:

            num_id = int(
                numbering_properties.numId.val
            )


        if numbering_properties.ilvl is not None:

            level = int(
                numbering_properties.ilvl.val
            )


        text = paragraph.text.strip()


        is_bulleted = (
            text.startswith("•")
            or text.startswith("-")
            or text.startswith("▪")
        )


        return Numbering(

            num_id=num_id,

            level=level,

            is_bulleted=is_bulleted,

            is_numbered=not is_bulleted,

            format=None,

            text=text if text else None,

            restart=False,

        )