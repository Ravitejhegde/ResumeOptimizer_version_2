from __future__ import annotations

import logging

from app.engine.writer.models.run_type import (
    RunType,
)

from app.engine.writer.models.write_context import (
    WriteContext,
)


logger = logging.getLogger(__name__)


class HyperlinkPreserver:
    """
    Validates hyperlink preservation.

    Pipeline:

        DocumentBuilder
              |
              v
        RunMapping
              |
              v
        HyperlinkPreserver
              |
              v
        DocxWriter


    Responsibilities:

        - Validate hyperlink metadata.
        - Ensure hyperlink runs are protected.
        - Prevent broken relationships.


    Does NOT:

        - Create hyperlinks.
        - Modify URLs.
        - Rewrite hyperlink text.
    """



    def preserve(
        self,
        context: WriteContext,
    ) -> None:
        """
        Validate hyperlink safety.
        """


        logger.info(
            "[HyperlinkPreserver] Checking hyperlinks..."
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

                        "Missing hyperlink relationship "
                        f"paragraph={paragraph.paragraph_index} "
                        f"run={run.run_index}"

                    )


                    continue



                # ----------------------------------
                # Target validation
                # ----------------------------------

                if not run.hyperlink_target:

                    context.add_error(

                        "Missing hyperlink target "
                        f"paragraph={paragraph.paragraph_index} "
                        f"run={run.run_index}"

                    )


                    continue



                # ----------------------------------
                # Protect hyperlink runs
                # ----------------------------------

                run.editable = False



                logger.debug(

                    "[HyperlinkPreserver] "
                    "Protected hyperlink=%s",

                    run.hyperlink_target,

                )



        logger.info(

            "[HyperlinkPreserver] "
            "Validated hyperlinks=%s",

            hyperlink_count,

        )