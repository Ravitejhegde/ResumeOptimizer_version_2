from app.services.document.snapshot.document_snapshot import (
    DocumentSnapshot,
)


class ParagraphSelector:
    """
    Selects paragraphs that should be optimized.

    Future versions will use semantic search.
    """

    KEYWORDS = {
        "summary",
        "profile",
        "objective",
        "skills",
        "experience",
        "project",
        "education",
    }

    @classmethod
    def select(
        cls,
        snapshot: DocumentSnapshot,
    ):

        selected = []

        for paragraph in snapshot.paragraphs:

            text = paragraph.text.lower()

            if any(
                keyword in text
                for keyword in cls.KEYWORDS
            ):
                selected.append(paragraph)

        return selected