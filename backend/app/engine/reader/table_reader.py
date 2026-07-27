from __future__ import annotations

from docx.table import Table as DocxTable

from app.engine.models.table import Table
from app.engine.models.paragraph import Paragraph
from app.engine.reader.run_reader import RunReader


class TableReader:
    """
    Reads a Word table into the engine Table model.

    Responsible ONLY for converting one table.
    """

    @staticmethod
    def read(
        docx_table: DocxTable,
        table_id: str,
    ) -> Table:

        rows = len(docx_table.rows)
        columns = len(docx_table.columns)

        cells: list[list[list[Paragraph]]] = []

        for row_index, row in enumerate(docx_table.rows):

            row_cells: list[list[Paragraph]] = []

            for column_index, cell in enumerate(row.cells):

                paragraphs: list[Paragraph] = []

                for paragraph_index, paragraph in enumerate(
                    cell.paragraphs
                ):

                    runs = [
                        RunReader.read(run)
                        for run in paragraph.runs
                    ]

                    paragraphs.append(

                        Paragraph(

                            id=(
                                f"{table_id}_"
                                f"R{row_index}"
                                f"C{column_index}"
                                f"P{paragraph_index}"
                            ),

                            runs=runs,

                            style_name=(
                                paragraph.style.name
                                if paragraph.style
                                else "Normal"
                            ),

                            alignment=(
                                str(paragraph.alignment)
                                if paragraph.alignment
                                else None
                            ),

                        )

                    )

                row_cells.append(
                    paragraphs
                )

            cells.append(
                row_cells
            )

        return Table(

            id=table_id,

            rows=rows,

            columns=columns,

            cells=cells,

            editable=True,

        )




