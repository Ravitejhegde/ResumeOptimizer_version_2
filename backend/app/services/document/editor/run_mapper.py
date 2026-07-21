from dataclasses import dataclass


@dataclass
class RunSlice:

    start: int

    end: int

    text: str


class RunMapper:
    """
    Maps existing Word runs into text slices.
    """

    @classmethod
    def map(cls, runs):

        result = []

        position = 0

        for run in runs:

            length = len(run.text)

            result.append(

                RunSlice(

                    start=position,

                    end=position + length,

                    text=run.text,

                )

            )

            position += length

        return result