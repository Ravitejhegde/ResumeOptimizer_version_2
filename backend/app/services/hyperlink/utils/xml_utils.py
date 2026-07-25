from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkUtils:
    """
    Common helper methods for hyperlinks.
    """

    @staticmethod
    def is_external(
        hyperlink: Hyperlink,
    ) -> bool:

        return bool(hyperlink.is_external)

    @staticmethod
    def has_url(
        hyperlink: Hyperlink,
    ) -> bool:

        return bool(hyperlink.url)

    @staticmethod
    def has_bookmark(
        hyperlink: Hyperlink,
    ) -> bool:

        return bool(hyperlink.bookmark)

    @staticmethod
    def display_text(
        hyperlink: Hyperlink,
    ) -> str:

        return hyperlink.text or ""

    @staticmethod
    def normalize_url(
        url: str,
    ) -> str:

        if not url:
            return ""

        return url.strip()

    @staticmethod
    def is_valid(
        hyperlink: Hyperlink,
    ) -> bool:

        if not hyperlink.relationship_id:
            return False

        if hyperlink.is_external:

            return bool(hyperlink.url)

        return True