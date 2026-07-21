from docx.table import _Cell

from app.services.document.models.cell_model import (
    CellModel,
)

from app.services.document.parser.paragraph_parser import (
    ParagraphParser,
)


class CellParser:
    """
    Parses Word table cells.
    """

    @classmethod
    def parse(
        cls,
        cells: list[_Cell],
        row_index: int,
    ) -> list[CellModel]:

        result = []

        for column_index, cell in enumerate(cells):

            model = CellModel()

            # -----------------------------------------
            # Identity
            # -----------------------------------------

            model.row = row_index

            model.column = column_index

            # -----------------------------------------
            # Size
            # -----------------------------------------

            try:

                if cell.width:

                    model.width = cell.width.pt

            except Exception:

                pass

            # -----------------------------------------
            # Cell Content
            # -----------------------------------------

            model.paragraphs = ParagraphParser.parse(
                cell.paragraphs
            )

            result.append(model)

        return result