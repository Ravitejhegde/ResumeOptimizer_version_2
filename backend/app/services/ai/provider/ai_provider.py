from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base interface for all AI providers.

    Every provider must implement generate().
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> str:
        pass