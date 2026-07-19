import re

from dataclasses import dataclass


@dataclass
class Hyperlink:

    text: str

    url: str

    paragraph_index: int

    block_id: int


class HyperlinkDetector:
    """
    Detect hyperlinks, emails and URLs from resume blocks.
    """

    EMAIL_PATTERN = re.compile(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    )

    URL_PATTERN = re.compile(

        r"(https?://[^\s]+|www\.[^\s]+|linkedin\.com/[^\s]+|github\.com/[^\s]+)",

        re.IGNORECASE,

    )

    @classmethod
    def detect(
        cls,
        blocks,
    ) -> list[Hyperlink]:

        links = []

        for block in blocks:

            text = block.text

            # -------------------------
            # Email
            # -------------------------

            for email in cls.EMAIL_PATTERN.findall(text):

                links.append(

                    Hyperlink(

                        text=email,

                        url=f"mailto:{email}",

                        paragraph_index=block.paragraph_index,

                        block_id=block.id,

                    )

                )

            # -------------------------
            # URLs
            # -------------------------

            for url in cls.URL_PATTERN.findall(text):

                actual = url

                if actual.startswith("www."):

                    actual = "https://" + actual

                links.append(

                    Hyperlink(

                        text=url,

                        url=actual,

                        paragraph_index=block.paragraph_index,

                        block_id=block.id,

                    )

                )

        return links