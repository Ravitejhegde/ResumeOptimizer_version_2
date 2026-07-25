from docx.shared import RGBColor

from app.core.logger import logger


class StyleWriter:
    """
    Restores hyperlink styling.

    Current version restores:

    - Color
    - Underline

    Future versions will restore:

    - Visited state
    - Hyperlink character style
    """

    @classmethod
    def restore(
        cls,
        run,
        hyperlink,
    ) -> None:

        try:

            if hyperlink.color:

                color = hyperlink.color.replace(
                    "#",
                    "",
                )

                if len(color) == 6:

                    run.font.color.rgb = (
                        RGBColor.from_string(
                            color
                        )
                    )

        except Exception as e:

            logger.debug(
                f"Color restore failed: {e}"
            )

        run.font.underline = (
            hyperlink.underline
        )

        try:

            if hyperlink.style:

                run.style = hyperlink.style

        except Exception:

            pass