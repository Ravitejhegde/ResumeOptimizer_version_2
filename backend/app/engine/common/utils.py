from __future__ import annotations

import uuid
from pathlib import Path


def generate_id() -> str:
    """
    Generate a unique identifier.
    """
    return str(uuid.uuid4())


def normalize_text(text: str) -> str:
    """
    Normalize text for comparisons.
    """
    return " ".join(text.split()).strip()


def is_blank(text: str | None) -> bool:
    """
    Returns True if text is None or empty.
    """
    return text is None or not text.strip()


def safe_string(value: object | None) -> str:
    """
    Convert any value into a safe string.
    """
    if value is None:
        return ""

    return str(value)


def file_extension(file_path: str | Path) -> str:
    """
    Return lowercase file extension.
    """
    return Path(file_path).suffix.lower()


def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if it does not exist.
    """
    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory




