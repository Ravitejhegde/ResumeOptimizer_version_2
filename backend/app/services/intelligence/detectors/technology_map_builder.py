from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)


class TechnologyMapBuilder:
    """
    Detect technologies once for every block.

    Returns

    {
        block_id: [
            "react",
            "typescript"
        ],

        block_id: [
            "git"
        ]
    }
    """

    @classmethod
    def build(
        cls,
        blocks,
    ):

        technology_map = {}

        for block in blocks:

            technology_map[
                block.id
            ] = TechnologyDetector.detect(
                block.text
            )

        return technology_map