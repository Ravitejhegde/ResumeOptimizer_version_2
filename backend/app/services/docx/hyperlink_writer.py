from app.core.logger import logger

from .hyperlink_restorer import (
    HyperlinkRestorer,
)


class HyperlinkWriter:
    """
    Coordinates hyperlink restoration.
    """

    @classmethod
    def restore(
        cls,
        paragraph,
        hyperlinks,
    ) -> None:

        if not hyperlinks:
            return

        logger.info(
            f"Restoring {len(hyperlinks)} hyperlink(s)"
        )

        HyperlinkRestorer.restore(
            paragraph=paragraph,
            hyperlinks=hyperlinks,
        )