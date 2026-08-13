"""
OpenRouter integration test.
"""

from app.ai.provider.provider_factory import (
    ProviderFactory,
)


def main() -> None:
    """
    Verify the configured AI provider works.
    """

    client = ProviderFactory.create()

    response = client.generate(
        "Reply with exactly: OpenRouter OK"
    )

    print("=" * 60)
    print("AI RESPONSE")
    print("=" * 60)
    print(response)


if __name__ == "__main__":
    main()