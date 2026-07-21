from app.services.document.snapshot.snapshot_builder import (
    SnapshotBuilder,
)

from app.services.document.snapshot.snapshot_index import (
    SnapshotIndex,
)

from app.services.intelligence.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)


class SnapshotService:
    """
    High-level access point for the Snapshot Engine.

    Responsibilities:
    - Build snapshots
    - Build indexes
    - Build resume knowledge
    - Provide search APIs
    """

    def __init__(
        self,
        snapshot,
    ):

        self.snapshot = snapshot

        self.index = SnapshotIndex(
            snapshot
        )

        self.knowledge = (
            KnowledgeBuilder.build(
                snapshot
            )
        )

    # -----------------------------------------
    # Factory
    # -----------------------------------------

    @classmethod
    def from_document(
        cls,
        document_model,
    ):

        snapshot = SnapshotBuilder.build(
            document_model
        )

        return cls(snapshot)

    # -----------------------------------------
    # Snapshot
    # -----------------------------------------

    def all_paragraphs(self):

        return self.snapshot.paragraphs

    # -----------------------------------------
    # Knowledge
    # -----------------------------------------

    def get_knowledge(self):

        return self.knowledge

    # -----------------------------------------
    # Paragraph
    # -----------------------------------------

    def paragraph(
        self,
        paragraph_id: str,
    ):

        return self.index.paragraph(
            paragraph_id
        )

    # -----------------------------------------
    # Search
    # -----------------------------------------

    def search(
        self,
        keyword: str,
    ):

        return self.index.search(
            keyword
        )

    # -----------------------------------------
    # Style
    # -----------------------------------------

    def style(
        self,
        style_name: str,
    ):

        return self.index.style(
            style_name
        )

    # -----------------------------------------
    # Count
    # -----------------------------------------

    def count(self) -> int:

        return len(
            self.snapshot.paragraphs
        )

    # -----------------------------------------
    # IDs
    # -----------------------------------------

    def ids(self):

        return [
            paragraph.id
            for paragraph in self.snapshot.paragraphs
        ]