import re


class TechnologyParser:
    """
    Extracts technologies without splitting
    multi-word technologies.
    """

    MULTI_WORD = [

        "html 5",
        "css 3",

        "node js",
        "node.js",
        "nodejs",

        "react js",
        "react.js",
        "reactjs",

        "vue js",
        "vue.js",
        "vuejs",

        "asp.net core",
        "asp.net",

        "machine learning",
        "deep learning",

        "computer vision",

        "natural language processing",

        "amazon web services",

        "google cloud",

        "github actions",

        "rest api",

        "ci/cd",

        "c sharp",

    ]

    @classmethod
    def tokenize(
        cls,
        text: str,
    ) -> list[str]:

        text = text.lower()

        found = []

        # ----------------------------------
        # Preserve multi-word technologies
        # ----------------------------------

        for tech in cls.MULTI_WORD:

            if tech in text:

                found.append(tech)

                text = text.replace(
                    tech,
                    " ",
                )

        # ----------------------------------
        # Remaining single words
        # ----------------------------------

        singles = re.findall(

            r"[a-zA-Z0-9.+#/-]+",

            text,

        )

        return found + singles