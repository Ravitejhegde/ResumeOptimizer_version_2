from docx.table import _Row

from app.services.document.models.row_model import (
    RowModel,
)

from app.services.document.parser.cell_parser import (
    CellParser,
)


class RowParser:
    """
    Parses Word table rows.
    """

    @classmethod
    def parse(
        cls,
        rows: list[_Row],
    ) -> list[RowModel]:

        result = []

        for index, row in enumerate(rows):

            model = RowModel()

            # -----------------------------------------
            # Identity
            # -----------------------------------------

            model.index = index

            # -----------------------------------------
            # Row Properties
            # -----------------------------------------

            try:

                if row.height:

                    model.height = row.height.pt

            except Exception:

                pass

            try:

                model.allow_break_across_pages = bool(
                    row.allow_break_across_pages
                )

            except Exception:

                model.allow_break_across_pages = True

            # -----------------------------------------
            # Cells
            # -----------------------------------------

            model.cells = CellParser.parse(
                row.cells,
                row_index=index,
            )

            result.append(model)

        return result