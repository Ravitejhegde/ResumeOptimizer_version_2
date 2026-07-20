from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)

from app.services.intelligence.technology.parser import (
    TechnologyParser,
)

from app.services.intelligence.technology.canonicalizer import (
    TechnologyCanonicalizer,
)


class TechnologyMapBuilder:
    """
    Detects, parses and normalizes technologies
    from every document block.

    Returns:

    {
        block_id: [
            "React",
            "TypeScript",
            "Node.js"
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

            detected = TechnologyDetector.detect(
                block.text
            )

            technologies = []

            for item in detected:

                parsed = TechnologyParser.tokenize(
                    item
                )

                for technology in parsed:

                    technology = (
                        TechnologyCanonicalizer.normalize(
                            technology
                        )
                    )

                    if (
                        technology
                        and technology not in technologies
                    ):
                        technologies.append(
                            technology
                        )

            technology_map[
                block.id
            ] = technologies

        return technology_map