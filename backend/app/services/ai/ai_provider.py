from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def optimize_paragraph(
        self,
        paragraph: str,
        job_description: str,
    ) -> str:
        pass