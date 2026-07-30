from __future__ import annotations

from docx.table import Table as DocxTable

from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.models.document.table import (
    Table,
)
from app.engine.reader.numbering_reader import (
    NumberingReader,
)
from app.engine.reader.run_reader import (
    RunReader,
)


class TableReader:
    """
    Reads a Word table into the engine Table model.

    Responsibilities:
        - Convert table structure.
        - Preserve cell paragraphs.
        - Preserve formatting.
        - Keep table editable.

    Does not:
        - Modify DOCX.
        - Optimize table content.
    """


    @staticmethod
    def read(
        docx_table: DocxTable,
        table_id: str,
    ) -> Table:
        """
        Convert python-docx table into engine Table.
        """

        if docx_table is None:
            raise ValueError(
                "DOCX table cannot be None."
            )


        rows = len(
            docx_table.rows
        )

        columns = len(
            docx_table.columns
        )


        cells: list[list[list[Paragraph]]] = []


        for row_index, row in enumerate(
            docx_table.rows
        ):

            row_cells: list[list[Paragraph]] = []


            for column_index, cell in enumerate(
                row.cells
            ):

                paragraphs: list[Paragraph] = []


                for paragraph_index, paragraph in enumerate(
                    cell.paragraphs
                ):

                    paragraph_id = (
                        f"{table_id}_"
                        f"R{row_index}_"
                        f"C{column_index}_"
                        f"P{paragraph_index}"
                    )


                    runs = [
                        RunReader.read(run)
                        for run in paragraph.runs
                    ]


                    engine_paragraph = Paragraph(

                        id=paragraph_id,

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


                        left_indent=(
                            paragraph.paragraph_format.left_indent.pt
                            if paragraph.paragraph_format.left_indent
                            else None
                        ),


                        right_indent=(
                            paragraph.paragraph_format.right_indent.pt
                            if paragraph.paragraph_format.right_indent
                            else None
                        ),


                        first_line_indent=(
                            paragraph.paragraph_format.first_line_indent.pt
                            if paragraph.paragraph_format.first_line_indent
                            else None
                        ),


                        space_before=(
                            paragraph.paragraph_format.space_before.pt
                            if paragraph.paragraph_format.space_before
                            else None
                        ),


                        space_after=(
                            paragraph.paragraph_format.space_after.pt
                            if paragraph.paragraph_format.space_after
                            else None
                        ),


                        line_spacing=(
                            float(
                                paragraph.paragraph_format.line_spacing
                            )
                            if paragraph.paragraph_format.line_spacing
                            else None
                        ),


                        numbering=(
                            NumberingReader.read(
                                paragraph
                            )
                        ),


                        editable=True,

                        section=None,

                    )


                    paragraphs.append(
                        engine_paragraph
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