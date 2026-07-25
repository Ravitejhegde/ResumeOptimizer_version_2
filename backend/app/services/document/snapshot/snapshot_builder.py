from app.services.document.snapshot.document_snapshot import (
    DocumentSnapshot,
)

from app.services.document.snapshot.hyperlink_snapshot import (
    HyperlinkSnapshot,
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

                # -------------------------------------
                # Runs
                # -------------------------------------

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

                # -------------------------------------
                # Hyperlinks
                # -------------------------------------

                hyperlinks = []

                for link in paragraph.hyperlinks:

                    hyperlinks.append(

                        HyperlinkSnapshot(

                            text=link.text,

                            url=link.url,

                            relationship_id=link.relationship_id,

                            is_external=link.is_external,

                            bookmark=link.bookmark,

                            email=link.email,

                            phone=link.phone,

                            tooltip=link.tooltip,

                            color=link.color,

                            underline=link.underline,

                            visited=link.visited,

                            style=link.style,

                            paragraph_id=link.paragraph_id,

                            run_index=link.run_index,

                        )

                    )

                # -------------------------------------
                # Paragraph Snapshot
                # -------------------------------------

                snapshot.paragraphs.append(

                    ParagraphSnapshot(

                        id=f"P{paragraph_id:05}",

                        style=paragraph.style,

                        text=paragraph.text,

                        runs=runs,

                        hyperlinks=hyperlinks,

                    )

                )

                paragraph_id += 1

        return snapshot