from pathlib import Path


class FilenameGenerator:
    """
    Generates unique filenames.

    Example:

    resume.docx
    resume(1).docx
    resume(2).docx
    """

    @classmethod
    def next_filename(
        cls,
        output_directory: str,
        original_filename: str,
    ) -> str:

        output_dir = Path(output_directory)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        original = Path(original_filename)

        stem = original.stem
        suffix = original.suffix

        candidate = output_dir / f"{stem}{suffix}"

        if not candidate.exists():
            return str(candidate)

        counter = 1

        while True:

            candidate = (
                output_dir
                / f"{stem}({counter}){suffix}"
            )

            if not candidate.exists():
                return str(candidate)

            counter += 1




