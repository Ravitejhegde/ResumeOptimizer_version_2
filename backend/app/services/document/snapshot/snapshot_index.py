from collections import defaultdict

from app.services.document.snapshot.document_snapshot import (
    DocumentSnapshot,
)

from app.services.document.snapshot.paragraph_snapshot import (
    ParagraphSnapshot,
)


class SnapshotIndex:
    """
    Fast lookup index for DocumentSnapshot.

    Supports:
    - Paragraph ID lookup
    - Text search
    - Style lookup
    """

    def __init__(
        self,
        snapshot: DocumentSnapshot,
    ):

        self.snapshot = snapshot

        self._paragraphs = {}

        self._styles = defaultdict(list)

        self._words = defaultdict(list)

        self._build()

    # -----------------------------------------
    # Build Index
    # -----------------------------------------

    def _build(self):

        for paragraph in self.snapshot.paragraphs:

            self._paragraphs[
                paragraph.id
            ] = paragraph

            self._styles[
                paragraph.style
            ].append(paragraph)

            for word in paragraph.text.lower().split():

                self._words[
                    word
                ].append(paragraph)

    # -----------------------------------------
    # Lookup by ID
    # -----------------------------------------

    def paragraph(
        self,
        paragraph_id: str,
    ) -> ParagraphSnapshot | None:

        return self._paragraphs.get(
            paragraph_id
        )

    # -----------------------------------------
    # Lookup by Style
    # -----------------------------------------

    def style(
        self,
        style_name: str,
    ) -> list[ParagraphSnapshot]:

        return self._styles.get(
            style_name,
            [],
        )

    # -----------------------------------------
    # Lookup by Word
    # -----------------------------------------

    def search(
        self,
        keyword: str,
    ) -> list[ParagraphSnapshot]:

        return self._words.get(
            keyword.lower(),
            [],
        )

    # -----------------------------------------
    # All Paragraphs
    # -----------------------------------------

    def paragraphs(
        self,
    ) -> list[ParagraphSnapshot]:

        return self.snapshot.paragraphs