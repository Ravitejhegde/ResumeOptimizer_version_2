"""
app.writer.models.writer_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the result of writing an optimized resume.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WriterResult:
    """
    Result produced by the Writer.
    """

    output_path: str = ""

    success: bool = False

    message: str = ""