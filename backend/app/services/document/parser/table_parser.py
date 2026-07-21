from docx.table import Table

from app.services.document.models.table_model import (
    TableModel,
)

from app.services.document.parser.row_parser import (
    RowParser,
)


class TableParser:
    """
    Parses Word tables into TableModel.
    """

    @classmethod
    def parse(
        cls,
        tables: list[Table],
    ) -> list[TableModel]:

        result = []

        for index, table in enumerate(tables):

            model = TableModel()

            # -----------------------------------------
            # Identity
            # -----------------------------------------

            model.index = index

            model.style = (
                table.style.name
                if table.style
                else ""
            )

            # -----------------------------------------
            # Table Properties
            # -----------------------------------------

            try:

                model.autofit = bool(
                    table.autofit
                )

            except Exception:

                model.autofit = True

            # -----------------------------------------
            # Rows
            # -----------------------------------------

            model.rows = RowParser.parse(
                table.rows
            )

            result.append(model)

        return result