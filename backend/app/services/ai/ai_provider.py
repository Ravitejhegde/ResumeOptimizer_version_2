from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base interface for AI providers.

    Providers are responsible only for
    sending prompts to an LLM and
    returning the raw response.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to the model and
        return the raw response.
        """
        raise NotImplementedError




