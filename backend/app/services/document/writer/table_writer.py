from docx.document import Document as DocxDocument

from app.services.document.models.table_model import (
    TableModel,
)

from app.services.document.writer.row_writer import (
    RowWriter,
)


class TableWriter:
    """
    Writes TableModel objects to DOCX.
    """

    @classmethod
    def write(
        cls,
        document: DocxDocument,
        tables: list[TableModel],
    ) -> None:

        for table_model in tables:

            if not table_model.rows:
                continue

            row_count = len(table_model.rows)

            column_count = max(
                (
                    len(row.cells)
                    for row in table_model.rows
                ),
                default=1,
            )

            table = document.add_table(
                rows=row_count,
                cols=column_count,
            )

            try:

                if table_model.style:

                    table.style = table_model.style

            except Exception:

                pass

            RowWriter.write(
                table,
                table_model.rows,
            )