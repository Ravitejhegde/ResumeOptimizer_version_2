from docx.table import Table

from app.services.document.models.row_model import (
    RowModel,
)

from app.services.document.writer.cell_writer import (
    CellWriter,
)


class RowWriter:
    """
    Writes RowModel objects into a Word table.
    """

    @classmethod
    def write(
        cls,
        table: Table,
        rows: list[RowModel],
    ) -> None:

        for row_model in rows:

            if row_model.index >= len(table.rows):
                continue

            row = table.rows[row_model.index]

            CellWriter.write(
                row,
                row_model.cells,
            )