from app.services.document.snapshot.document_snapshot import (
    DocumentSnapshot,
)

from app.services.document.snapshot.paragraph_snapshot import (
    ParagraphSnapshot,
)

from app.services.document.snapshot.run_snapshot import (
    RunSnapshot,
)


class SnapshotBuilder:
    """
    Converts parsed DocumentModel into an immutable
    DocumentSnapshot used by the Intelligence Engine.
    """

    @classmethod
    def build(
        cls,
        document_model,
    ) -> DocumentSnapshot:

        snapshot = DocumentSnapshot()

        paragraph_id = 1

        for section in document_model.sections:

            for paragraph in section.paragraphs:

                runs = []

                for run in paragraph.runs:

                    runs.append(

                        RunSnapshot(

                            text=run.text,

                            bold=run.bold,

                            italic=run.italic,

                            underline=run.underline,

                            font=run.font_name,

                            size=run.font_size,

                        )

                    )

                snapshot.paragraphs.append(

                    ParagraphSnapshot(

                        id=f"P{paragraph_id:05}",

                        style=paragraph.style,

                        text=paragraph.text,

                        runs=runs,

                    )

                )

                paragraph_id += 1

        return snapshot