import re


class FactValidator:

    @staticmethod
    def validate(
        original: str,
        optimized: str,
    ) -> tuple[bool, str]:

        original_words = {

            word.lower()

            for word in re.findall(
                r"[A-Za-z0-9.+#-]+",
                original,
            )

        }

        optimized_words = {

            word.lower()

            for word in re.findall(
                r"[A-Za-z0-9.+#-]+",
                optimized,
            )

        }

        new_words = optimized_words - original_words

        if len(new_words) > 5:

            return (

                False,

                f"Too many new words introduced: {', '.join(sorted(new_words)[:5])}"

            )

        return True, "Safe"