from __future__ import annotations

import logging

from app.engine.writer.models.run_type import (
    RunType,
)

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class HyperlinkValidator:
    """
    Validates hyperlink integrity before DOCX saving.

    Pipeline:

        HyperlinkPreserver
                |
                v
        HyperlinkValidator
                |
                v
            DocxWriter


    Responsibilities:

        - Ensure hyperlink metadata exists.
        - Prevent broken hyperlink output.
        - Validate relationship references.


    Does NOT:

        - Create hyperlinks.
        - Modify hyperlinks.
        - Change document content.
    """



    def validate(
        self,
        context: WriteContext,
    ) -> None:
        """
        Validate all hyperlink mappings.
        """


        logger.info(
            "[HyperlinkValidator] "
            "Validating hyperlinks..."
        )


        hyperlink_count = 0



        for paragraph in context.paragraph_mappings:


            for run in paragraph.run_mappings:


                if run.run_type != RunType.HYPERLINK:

                    continue


                hyperlink_count += 1



                # ----------------------------------
                # Relationship validation
                # ----------------------------------

                if not run.relationship_id:

                    context.add_error(

                        "Hyperlink missing relationship id "
                        f"(paragraph={paragraph.paragraph_index}, "
                        f"run={run.run_index})"

                    )



                # ----------------------------------
                # Target validation
                # ----------------------------------

                if not run.hyperlink_target:

                    context.add_error(

                        "Hyperlink missing target "
                        f"(paragraph={paragraph.paragraph_index}, "
                        f"run={run.run_index})"

                    )



        logger.info(

            "[HyperlinkValidator] "
            "Validated hyperlinks=%s",

            hyperlink_count,

        )