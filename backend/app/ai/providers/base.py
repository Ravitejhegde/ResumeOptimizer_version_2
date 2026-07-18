from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def optimize_section(
        self,
        prompt: str,
        section_content: str,
        job_description: str,
    ) -> str:
        pass