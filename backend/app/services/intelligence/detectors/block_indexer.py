from collections import defaultdict


class BlockIndexer:
    """
    Groups blocks by section.

    Input

    [
        {
            "block": ...,
            "section": "SUMMARY"
        },
        {
            "block": ...,
            "section": "SKILLS"
        }
    ]

    Output

    {
        "SUMMARY":[...],
        "SKILLS":[...]
    }
    """

    @staticmethod
    def build(

        detected_sections,

    ):

        grouped = defaultdict(list)

        for item in detected_sections:

            grouped[
                item["section"]
            ].append(item)

        return dict(grouped)