from docx.text.paragraph import Paragraph


class WordMapper:

    @staticmethod
    def distribute(
        paragraph: Paragraph,
        new_text: str,
    ):

        runs = paragraph.runs

        if not runs:

            paragraph.add_run(
                new_text,
            )

            return

        words = new_text.split()

        if not words:

            return

        run_count = len(runs)

        words_per_run = max(
            1,
            len(words) // run_count,
        )

        index = 0

        for run in runs:

            run.text = " ".join(

                words[
                    index:
                    index + words_per_run
                ]

            )

            index += words_per_run

        if index < len(words):

            runs[-1].text += (
                " "
                + " ".join(
                    words[index:]
                )
            )