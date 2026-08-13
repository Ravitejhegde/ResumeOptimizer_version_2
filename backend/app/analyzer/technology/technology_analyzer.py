"""
app.analyzer.technology.technology_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detect technologies from a parsed resume.
"""

from __future__ import annotations

from app.analyzer.contracts.technology_analyzer_contract import (
    TechnologyAnalyzerContract,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.technology_model import (
    TechnologyModel,
)
from app.analyzer.technology.technology_detector import (
    TechnologyDetector,
)


class TechnologyAnalyzer(
    TechnologyAnalyzerContract,
):
    """
    Detect technologies from every resume section.
    """

    def __init__(self) -> None:
        self._detector = TechnologyDetector()

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:

        document.technologies.clear()

        for section_name, section in document.sections.items():

            detected = self._detector.detect(
                section.text
            )

            for technology_id in detected:

                if technology_id not in document.technologies:

                    document.technologies[
                        technology_id
                    ] = TechnologyModel(
                        id=technology_id,
                        name=technology_id.replace(
                            "_",
                            " ",
                        ).title(),
                        section=section_name,
                    )

        return document