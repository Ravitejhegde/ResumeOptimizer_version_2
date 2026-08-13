"""
Runtime validation.
"""

from __future__ import annotations

from app.knowledge.bootstrap import get_runtime


def validate_runtime() -> None:
    """
    Validate runtime startup.
    """

    runtime = get_runtime()

    assert runtime.is_loaded

    print("✓ Runtime Loaded")

    print(
        f"Roles: {len(runtime.roles.all())}"
    )

    print(
        f"Skills: {len(runtime.skills.all())}"
    )

    print(
        f"Categories: {len(runtime.categories.all())}"
    )

    print(
        f"Technologies: {len(runtime.technologies.all())}"
    )


if __name__ == "__main__":
    validate_runtime()