from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)


class HyperlinkValidator:
    """
    Validates Hyperlink objects before they are
    written back into the document.
    """

    @classmethod
    def validate(
        cls,
        hyperlink: Hyperlink,
    ) -> bool:

        # Relationship ID is required
        if not hyperlink.relationship_id:
            return False

        # Hyperlink text should exist
        if hyperlink.text is None:
            return False

        # External links require a URL
        if hyperlink.is_external and not hyperlink.url:
            return False

        return True