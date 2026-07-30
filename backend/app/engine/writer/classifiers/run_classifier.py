from __future__ import annotations

from docx.document import Document as DocxDocument

from app.engine.writer.helpers.relationship_helper import (
    RelationshipHelper,
)
from app.engine.writer.helpers.xml_helper import (
    XMLHelper,
)
from app.engine.writer.models.run_mapping import (
    RunMapping,
)
from app.engine.writer.models.run_type import (
    RunType,
)


class RunClassifier:
    """
    Classifies DOCX runs and extracts metadata.

    Every run is classified exactly once while building
    the WriteContext.
    """

    def classify(
        self,
        mapping: RunMapping,
        document: DocxDocument,
    ) -> None:

        run = mapping.docx_run

        # -------------------------
        # Hyperlink
        # -------------------------
        relationship_id = RelationshipHelper.get_relationship_id(run)

        if relationship_id is not None:
            mapping.run_type = RunType.HYPERLINK
            mapping.editable = False
            mapping.relationship_id = relationship_id
            mapping.hyperlink_target = (
                RelationshipHelper.get_hyperlink_target(
                    document,
                    relationship_id,
                )
            )
            return

        # -------------------------
        # Tab
        # -------------------------
        if XMLHelper.has_tab(run):
            mapping.run_type = RunType.TAB
            mapping.editable = False
            return

        # -------------------------
        # Line Break
        # -------------------------
        if XMLHelper.has_line_break(run):
            mapping.run_type = RunType.LINE_BREAK
            mapping.editable = False
            return

        # -------------------------
        # Image / Drawing
        # -------------------------
        if XMLHelper.has_drawing(run):
            mapping.run_type = RunType.IMAGE
            mapping.editable = False
            return

        # -------------------------
        # Field
        # -------------------------
        if XMLHelper.has_field(run):
            mapping.run_type = RunType.FIELD
            mapping.editable = False
            return

        # -------------------------
        # Bookmark
        # -------------------------
        if XMLHelper.has_bookmark(run):
            mapping.run_type = RunType.BOOKMARK
            mapping.editable = False
            return

        # -------------------------
        # Default
        # -------------------------
        mapping.run_type = RunType.TEXT
        mapping.editable = True