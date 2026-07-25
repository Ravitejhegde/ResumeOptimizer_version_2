from docx.oxml.ns import qn


class HyperlinkXML:
    """
    Utilities for working with Word hyperlink XML.

    This class never modifies text.
    It only locates and inspects hyperlink
    elements inside a paragraph.

    Future versions will support:
    - Restoring hyperlinks
    - Rebuilding relationship IDs
    - Updating hyperlink text
    - Preserving formatting
    """

    @classmethod
    def find_all(
        cls,
        paragraph,
    ) -> list:

        return paragraph._p.findall(
            qn("w:hyperlink")
        )

    @classmethod
    def has_hyperlinks(
        cls,
        paragraph,
    ) -> bool:

        return len(
            cls.find_all(paragraph)
        ) > 0

    @classmethod
    def count(
        cls,
        paragraph,
    ) -> int:

        return len(
            cls.find_all(paragraph)
        )