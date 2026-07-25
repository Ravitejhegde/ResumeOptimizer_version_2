from app.core.logger import logger


class HyperlinkUtils:
    """
    Utility methods for working with hyperlinks.

    These methods never modify the document.
    They only inspect hyperlink information.
    """

    @staticmethod
    def is_valid(link) -> bool:

        return bool(
            link
            and link.text
            and link.url
        )

    @staticmethod
    def normalize(url: str) -> str:

        if not url:
            return ""

        url = url.strip()

        if url.startswith("http://"):
            return url

        if url.startswith("https://"):
            return url

        if url.startswith("mailto:"):
            return url

        if url.startswith("tel:"):
            return url

        return "https://" + url

    @staticmethod
    def log(link) -> None:

        logger.info(
            f"{link.text} -> {link.url}"
        )